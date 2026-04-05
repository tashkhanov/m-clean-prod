"""
Утилиты для админки: сжатие изображений в WebP.
"""
import os
from io import BytesIO

from django.contrib import messages
from PIL import Image


def compress_to_webp(modeladmin, request, queryset):
    """
    Admin Action: Конвертирует изображения выбранных записей в WebP.
    
    Ищет все ImageField в модели, конвертирует JPG/PNG в WebP (quality=75),
    удаляет старый файл и сохраняет новый путь в БД.
    """
    quality = 75
    converted = 0
    skipped = 0
    errors = 0
    
    # Находим все ImageField в модели
    image_fields = [
        field.name for field in queryset.model._meta.get_fields()
        if field.get_internal_type() == 'ImageField'
    ]
    
    if not image_fields:
        messages.warning(request, 'В выбранной модели нет полей с изображениями.')
        return
    
    for obj in queryset:
        for field_name in image_fields:
            image_field = getattr(obj, field_name)
            
            # Пропускаем пустые поля
            if not image_field:
                continue
            
            try:
                file_path = image_field.path
                file_ext = os.path.splitext(file_path)[1].lower()
                
                # Пропускаем уже WebP
                if file_ext == '.webp':
                    skipped += 1
                    continue
                
                # Пропускаем не JPG/PNG
                if file_ext not in ['.jpg', '.jpeg', '.png']:
                    skipped += 1
                    continue
                
                # Открываем и конвертируем
                with Image.open(file_path) as img:
                    # Конвертируем в RGB если нужно (для PNG с прозрачностью)
                    if img.mode in ('RGBA', 'P'):
                        img = img.convert('RGB')
                    
                    # Сохраняем в WebP
                    buffer = BytesIO()
                    img.save(buffer, format='WEBP', quality=quality, method=6)
                    buffer.seek(0)
                    
                    # Генерируем новое имя файла
                    old_name = os.path.basename(file_path)
                    new_name = os.path.splitext(old_name)[0] + '.webp'
                    
                    # Сохраняем
                    image_field.save(new_name, buffer, save=False)
                    obj.save(update_fields=[field_name])
                    
                    # Удаляем старый файл
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    
                    converted += 1
            
            except Exception as e:
                errors += 1
                messages.error(request, f'Ошибка при обработке {obj}: {str(e)}')
    
    # Формируем сообщение
    if converted > 0:
        messages.success(request, f'Изображения успешно сжаты! Конвертировано: {converted}')
    if skipped > 0:
        messages.info(request, f'Пропущено (уже WebP или не JPG/PNG): {skipped}')
    if errors > 0:
        messages.error(request, f'Ошибок: {errors}')
    if converted == 0 and skipped > 0 and errors == 0:
        messages.info(request, 'Все изображения уже в формате WebP.')


compress_to_webp.short_description = "Сжать изображения (WebP)"
