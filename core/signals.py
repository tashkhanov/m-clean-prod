import io
import os

from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.core.files.base import ContentFile
from PIL import Image


# ═══════════════════════════════════════════════════════════════
# УДАЛЕНИЕ СТАРЫХ ФАЙЛОВ
# ═══════════════════════════════════════════════════════════════

def delete_old_file(instance, field_name):
    """Удаляет старый файл при замене изображения."""
    try:
        model = instance.__class__
        old_instance = model.objects.get(pk=instance.pk)
        old_field = getattr(old_instance, field_name)
        new_field = getattr(instance, field_name)
        
        if old_field and old_field != new_field:
            if os.path.isfile(old_field.path):
                os.remove(old_field.path)
    except Exception:
        pass


def delete_file_on_delete(instance, field_name):
    """Удаляет файл при удалении записи."""
    try:
        field = getattr(instance, field_name)
        if field and hasattr(field, 'path'):
            if os.path.isfile(field.path):
                os.remove(field.path)
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════
# КОНВЕРТАЦИЯ В WEBP
# ═══════════════════════════════════════════════════════════════

def convert_to_webp(image_field):
    """Конвертирует изображение в WebP формат. Возвращает ContentFile или None."""
    if not image_field:
        return None

    ext = os.path.splitext(image_field.name)[1].lower()
    if ext == '.webp':
        return None

    try:
        image_field.open()
        img = Image.open(image_field)

        if img.mode in ('RGBA', 'P', 'LA'):
            if img.mode == 'P':
                img = img.convert('RGBA')
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = rgb_img
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        buffer = io.BytesIO()
        img.save(buffer, format='WEBP', quality=85, method=6)
        buffer.seek(0)

        base_name = os.path.splitext(os.path.basename(image_field.name))[0]
        new_name = f"{base_name}.webp"

        return ContentFile(buffer.read(), name=new_name)
    except Exception as e:
        print(f"Ошибка конвертации WebP: {e}")
        return None


# ═══════════════════════════════════════════════════════════════
# СИГНАЛЫ ДЛЯ ВСЕХ МОДЕЛЕЙ
# ═══════════════════════════════════════════════════════════════

def handle_image_save(sender, instance, **kwargs):
    """Удаляет старый файл и конвертирует новый в WebP."""
    for field in sender._meta.fields:
        if field.get_internal_type() == 'ImageField':
            field_name = field.name
            
            # Удаляем старый файл
            delete_old_file(instance, field_name)
            
            # Конвертируем новый в WebP
            current_file = getattr(instance, field_name)
            if not current_file:
                continue

            try:
                old_instance = sender.objects.get(pk=instance.pk)
                old_file = getattr(old_instance, field_name)
                if old_file and old_file.name == current_file.name:
                    continue
            except sender.DoesNotExist:
                pass

            result = convert_to_webp(current_file)
            if result:
                setattr(instance, field_name, result)


def handle_image_delete(sender, instance, **kwargs):
    """Удаляет файлы при удалении записи."""
    for field in sender._meta.fields:
        if field.get_internal_type() == 'ImageField':
            delete_file_on_delete(instance, field.name)


def register_image_signals():
    """Регистрирует сигналы для всех моделей."""
    from core.models import SiteSettings, TeamMember, Certificate, Discount, Equipment, Chemical, Partner
    from services.models import Service, Category
    from portfolio.models import WorkCase, Review
    from blog.models import Post

    models_to_watch = [
        SiteSettings, TeamMember, Certificate, Discount, Equipment, Chemical, Partner,
        Service, Category, WorkCase, Review, Post
    ]

    for model_cls in models_to_watch:
        pre_save.connect(handle_image_save, sender=model_cls, dispatch_uid=f'image_save_{model_cls.__name__}')
        post_delete.connect(handle_image_delete, sender=model_cls, dispatch_uid=f'image_delete_{model_cls.__name__}')
