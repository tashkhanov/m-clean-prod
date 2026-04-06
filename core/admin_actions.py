import sys
from django.contrib import messages
from .utils import optimize_image_field

def compress_images_action(modeladmin, request, queryset, image_fields=None, quality=75):
    """
    Улучшенный экшен для WebP + Watermark + Smart Crop (16:10):
    - Ищет ватермарк во всех записях настроек.
    - Для работ Портфолио принудительно делает обрезку 16:10.
    """
    from core.models import SiteSettings
    
    if image_fields is None:
        image_fields = ['image']
    
    settings = SiteSettings.objects.exclude(watermark='').first()
    master_watermark = settings.watermark if settings else None
    
    if master_watermark:
        messages.info(request, f"Система: Ватермарк найден. Приступаю к обрезке 16:10 и наложению лого.")
    else:
        messages.warning(request, "Система: Логотип не найден. Будет выполнена только обрезка 16:10 и WebP.")

    converted = 0
    skipped = 0
    errors = 0
    
    for obj in queryset:
        model_name = obj._meta.model_name
        
        for field_name in image_fields:
            try:
                watermark_to_use = None
                # Для Портфолио всегда включаем умную обрезку 16:10
                is_portfolio = (model_name == 'workcase' and field_name in ['image_before', 'image_after'])
                
                if is_portfolio:
                    watermark_to_use = master_watermark
                
                # Если не портфолио и уже WebP — пропускаем
                if not is_portfolio:
                    image_field = getattr(obj, field_name, None)
                    if image_field and image_field.name.lower().endswith('.webp'):
                        skipped += 1
                        continue

                # Обработка с флагом force_16_10 для Портфолио
                if optimize_image_field(
                    obj, field_name, 
                    watermark_file=watermark_to_use, 
                    quality=quality,
                    force_16_10=is_portfolio
                ):
                    converted += 1
                else:
                    skipped += 1
                    
            except Exception as e:
                errors += 1
                sys.stderr.write(f"Error processing {obj}: {e}\n")
                messages.error(request, f'Ошибка: {str(e)}')
    
    if converted > 0:
        messages.success(request, f'Успешно обработано (WebP + 16:10 Crop): {converted}')
    if skipped > 0:
        messages.info(request, f'Пропущено: {skipped}')
    if errors > 0:
        messages.error(request, f'Ошибок: {errors}')


def make_compress_action(image_fields=None, quality=75, short_description=None):
    def compress_action(modeladmin, request, queryset):
        compress_images_action(modeladmin, request, queryset, image_fields, quality)
    compress_action.short_description = short_description or 'Сжать изображения (WebP)'
    compress_action.allowed_permissions = ['change']
    return compress_action

# Регистрация экшенов
compress_service_images = make_compress_action(image_fields=['image'], short_description='Сжать изображения услуги (WebP)')
compress_workcase_images = make_compress_action(image_fields=['image_before', 'image_after'], short_description='Сжать изображения работы (WebP + 16:10 Crop + Watermark)')
compress_partner_logos = make_compress_action(image_fields=['logo'], quality=80, short_description='Сжать логотип партнёра (WebP)')
compress_team_photos = make_compress_action(image_fields=['photo'], short_description='Сжать фото сотрудника (WebP)')
compress_certificate_images = make_compress_action(image_fields=['image'], short_description='Сжать изображение сертификата (WebP)')
compress_discount_images = make_compress_action(image_fields=['image'], short_description='Сжать изображение акции (WebP)')
compress_equipment_photos = make_compress_action(image_fields=['photo'], short_description='Сжать фото оборудования (WebP)')
compress_site_images = make_compress_action(image_fields=['logo', 'logo_footer', 'favicon', 'hero_image', 'watermark'], quality=80, short_description='Сжать изображения сайта (WebP)')
compress_chemical_photos = make_compress_action(image_fields=['photo'], short_description='Сжать фото химии (WebP)')
