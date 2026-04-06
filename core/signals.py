import os
from django.db.models.signals import pre_save, post_delete
from django.apps import apps


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
            if hasattr(old_field, 'path') and os.path.isfile(old_field.path):
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
# СИГНАЛЫ ДЛЯ ВСЕХ МОДЕЛЕЙ (Очистка файлов)
# ═══════════════════════════════════════════════════════════════

def handle_image_delete(sender, instance, **kwargs):
    """Удаляет файлы при удалении модели."""
    for field in sender._meta.fields:
        if field.get_internal_type() == 'ImageField':
            delete_file_on_delete(instance, field.name)


def handle_old_image_cleanup(sender, instance, **kwargs):
    """Удаляет старые файлы при замене поля изображения."""
    if not instance.pk:
        return
    for field in sender._meta.fields:
        if field.get_internal_type() == 'ImageField':
            delete_old_file(instance, field.name)


def register_image_signals():
    """
    Регистрирует сигналы для очистки файлов.
    АВТО-ОПТИМИЗАЦИЯ ОТКЛЮЧЕНА согласно запросу пользователя.
    """
    # Собираем все модели, у которых есть ImageField
    for model in apps.get_models():
        has_image_field = any(f.get_internal_type() == 'ImageField' for f in model._meta.fields)
        if has_image_field:
            # Чистим старые файлы при замене
            pre_save.connect(handle_old_image_cleanup, sender=model, dispatch_uid=f'cleanup_save_{model._meta.label}')
            # Чистим файлы при удалении
            post_delete.connect(handle_image_delete, sender=model, dispatch_uid=f'cleanup_delete_{model._meta.label}')
