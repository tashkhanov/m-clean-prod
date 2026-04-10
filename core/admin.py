import os
from io import BytesIO

from django.contrib import admin, messages
from django.core.files.base import ContentFile
from PIL import Image
from unfold.admin import ModelAdmin

from .models import SiteSettings, Faq, Partner, BeforeAfter, Service, TeamMember, Certificate, ServicePackage, Equipment, Chemical, Discount, CompanyFact
from .admin_actions import (
    compress_site_images,
    compress_partner_logos,
    compress_team_photos,
    compress_certificate_images,
    compress_discount_images,
    compress_equipment_photos,
    compress_chemical_photos,
    compress_service_images,
)


def compress_image_to_webp(image_field, quality=80):
    """
    Конвертирует изображение в WebP формат.
    Возвращает (success: bool, new_name: str or None, old_path: str or None)
    """
    if not image_field:
        return False, None, None
    
    try:
        file_path = image_field.path
        file_ext = os.path.splitext(file_path)[1].lower()
        
        # Пропускаем если уже WebP
        if file_ext == '.webp':
            return False, None, None
        
        # Проверяем формат
        if file_ext not in ['.jpg', '.jpeg', '.png']:
            return False, None, None
        
        # Открываем и конвертируем
        with Image.open(file_path) as img:
            # Конвертируем RGBA/P в RGB для WebP
            if img.mode in ('RGBA', 'P', 'LA'):
                img = img.convert('RGB')
            
            # Сохраняем в WebP
            buffer = BytesIO()
            img.save(buffer, format='WEBP', quality=quality, method=6)
            buffer.seek(0)
            
            # Новое имя файла
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            new_name = f"{base_name}.webp"
            
            return True, new_name, file_path, buffer.read()
    
    except Exception as e:
        return False, None, None, str(e)


def compress_images_action(modeladmin, request, queryset):
    """
    Admin action для сжатия изображений выбранных записей в WebP.
    Ищет все ImageField в модели и конвертирует их.
    """
    from django.db import models
    
    quality = 80
    converted = 0
    skipped = 0
    errors = 0
    
    # Находим все ImageField в модели
    image_fields = []
    for field in queryset.model._meta.get_fields():
        if isinstance(field, models.ImageField):
            image_fields.append(field.name)
    
    if not image_fields:
        messages.warning(request, "В этой модели нет полей с изображениями.")
        return
    
    for obj in queryset:
        for field_name in image_fields:
            image_field = getattr(obj, field_name, None)
            if not image_field:
                continue
            
            try:
                file_path = image_field.path
                file_ext = os.path.splitext(file_path)[1].lower()
                
                # Пропускаем WebP
                if file_ext == '.webp':
                    skipped += 1
                    continue
                
                # Пропускаем не JPG/PNG
                if file_ext not in ['.jpg', '.jpeg', '.png']:
                    skipped += 1
                    continue
                
                # Конвертируем
                with Image.open(file_path) as img:
                    if img.mode in ('RGBA', 'P', 'LA'):
                        img = img.convert('RGB')
                    
                    buffer = BytesIO()
                    img.save(buffer, format='WEBP', quality=quality, method=6)
                    buffer.seek(0)
                    
                    base_name = os.path.splitext(os.path.basename(file_path))[0]
                    new_name = f"{base_name}.webp"
                    
                    # Сохраняем новый файл
                    image_field.save(new_name, ContentFile(buffer.read()), save=False)
                    obj.save(update_fields=[field_name])
                    
                    # Удаляем старый файл
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    
                    converted += 1
            
            except Exception as e:
                errors += 1
                messages.error(request, f"Ошибка при обработке {obj}: {str(e)}")
    
    # Итоговое сообщение
    if converted > 0:
        messages.success(request, f"Изображения успешно сжаты! Конвертировано: {converted}, пропущено: {skipped}.")
    elif skipped > 0 and errors == 0:
        messages.info(request, f"Все изображения уже в WebP формате. Пропущено: {skipped}.")
    else:
        messages.warning(request, f"Конвертировано: {converted}, пропущено: {skipped}, ошибок: {errors}.")


compress_images_action.short_description = "Сжать изображения (WebP)"


def get_compress_action():
    """Возвращает action функцию для использования в ModelAdmin."""
    return compress_images_action


# ═══════════════════════════════════════════════════════════════
# ADMIN CLASSES
# ═══════════════════════════════════════════════════════════════

@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    list_display = ('company_name', 'phone', 'email')
    actions = [compress_images_action]
    fieldsets = (
        ("Брендинг", {
            'fields': ('logo', 'logo_footer', 'favicon', 'hero_image'),
            'description': "Логотипы и главное фото Hero-секции"
        }),
        ("Hero секция (Главный экран)", {
            'fields': ('hero_title', 'hero_subtitle'),
            'description': "Заголовок и подзаголовок на первом экране. HTML разрешён."
        }),
        ("О компании", {
            'fields': ('company_name', 'tagline', 'about_short'),
        }),
        ("Контакты", {
            'fields': ('phone', 'phone_secondary', 'email', 'address', 'working_hours', 'min_order'),
        }),
        ("Социальные сети", {
            'fields': ('whatsapp_phone', 'telegram', 'instagram', 'vk'),
        }),
        ("Рейтинги и Отзывы", {
            'fields': (
                ('rating_yandex', 'url_reviews_yandex'),
                ('rating_google', 'url_reviews_google'),
                ('rating_2gis', 'url_reviews_2gis'),
            ),
            'description': "Укажите ссылки на страницы отзывов и средний рейтинг (для отображения звезд)"
        }),
        ("Уведомления Telegram", {
            'fields': ('telegram_bot_token', 'telegram_chat_id'),
            'description': "Для получения уведомлений о новых заявках"
        }),
        ("SEO и ресурсы", {
            'fields': ('seo_title', 'seo_description', 'video', 'watermark'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Faq)
class FaqAdmin(ModelAdmin):
    list_display = ('question', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('question',)
    list_filter = ('is_active',)


@admin.register(Partner)
class PartnerAdmin(ModelAdmin):
    list_display = ('name', 'url', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('name',)
    actions = [compress_images_action]


@admin.register(BeforeAfter)
class BeforeAfterAdmin(ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title',)
    actions = [compress_images_action]


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ('title', 'icon', 'price_from', 'order', 'is_active')
    list_editable = ('order', 'is_active', 'price_from')
    search_fields = ('title',)
    list_filter = ('icon', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    actions = [compress_images_action]
    fieldsets = (
        ("Основное", {
            'fields': ('icon', 'title', 'slug', 'short_description', 'description', 'price_from', 'image'),
        }),
        ("Видео", {
            'fields': ('video_url',),
            'classes': ('collapse',),
        }),
        ("SEO", {
            'fields': ('meta_title', 'meta_description', 'og_image'),
            'classes': ('collapse',),
        }),
        ("Отображение", {
            'fields': ('order', 'is_active'),
        }),
    )


class ServicePackageInline(admin.TabularInline):
    model = ServicePackage
    extra = 1
    fields = ('tier', 'price', 'unit', 'features')


@admin.register(ServicePackage)
class ServicePackageAdmin(ModelAdmin):
    list_display = ('service', 'tier', 'price', 'unit')
    list_filter = ('tier', 'service')
    search_fields = ('service__title',)


@admin.register(Equipment)
class EquipmentAdmin(ModelAdmin):
    list_display = ('name', 'brand', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'brand')
    actions = [compress_images_action]
    fieldsets = (
        ("Основное", {
            'fields': ('name', 'brand', 'photo', 'photo_alt', 'description'),
        }),
        ("Характеристики", {
            'fields': ('features',),
            'classes': ('collapse',),
        }),
        ("Отображение", {
            'fields': ('order', 'is_active'),
        }),
    )


@admin.register(Chemical)
class ChemicalAdmin(ModelAdmin):
    list_display = ('name', 'brand', 'eco_status', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('eco_status', 'is_active')
    search_fields = ('name', 'brand')
    actions = [compress_images_action]


@admin.register(Discount)
class DiscountAdmin(ModelAdmin):
    list_display = ('title', 'discount_percent', 'discount_amount', 'valid_until', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('title',)
    actions = [compress_images_action]
    fieldsets = (
        ("Основное", {
            'fields': ('title', 'description', 'image', 'image_alt'),
        }),
        ("Скидка", {
            'fields': ('discount_percent', 'discount_amount', 'valid_until'),
        }),
        ("Отображение", {
            'fields': ('order', 'is_active'),
        }),
    )




@admin.register(TeamMember)
class TeamMemberAdmin(ModelAdmin):
    list_display = ('name', 'position', 'experience_years', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('position', 'is_active')
    search_fields = ('name',)
    actions = [compress_images_action]
    fieldsets = (
        ("Основное", {
            'fields': ('name', 'position', 'experience_years', 'photo', 'photo_alt'),
        }),
        ("Дополнительно", {
            'fields': ('bio',),
            'classes': ('collapse',),
        }),
        ("Отображение", {
            'fields': ('order', 'is_active'),
        }),
    )


@admin.register(Certificate)
class CertificateAdmin(ModelAdmin):
    list_display = ('title', 'issued_by', 'issued_date', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'issued_by')
    actions = [compress_images_action]
    fieldsets = (
        ("Основное", {
            'fields': ('title', 'image', 'image_alt', 'issued_by', 'issued_date'),
        }),
        ("Отображение", {
            'fields': ('order', 'is_active'),
        }),
    )


@admin.register(CompanyFact)
class CompanyFactAdmin(ModelAdmin):
    list_display = ('label', 'value', 'suffix', 'icon', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('icon', 'is_active')
    search_fields = ('label',)
