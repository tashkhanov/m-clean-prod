from django.contrib import admin
from django.contrib import messages
from django.core.files.base import ContentFile
from unfold.admin import ModelAdmin
from PIL import Image
import os
from io import BytesIO

from .models import WorkCase, Review


def compress_images_action(modeladmin, request, queryset):
    """
    Admin action для сжатия изображений выбранных записей в WebP.
    """
    from django.db import models
    
    quality = 80
    converted = 0
    skipped = 0
    
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
                
                if file_ext == '.webp':
                    skipped += 1
                    continue
                
                if file_ext not in ['.jpg', '.jpeg', '.png']:
                    skipped += 1
                    continue
                
                with Image.open(file_path) as img:
                    if img.mode in ('RGBA', 'P', 'LA'):
                        img = img.convert('RGB')
                    
                    buffer = BytesIO()
                    img.save(buffer, format='WEBP', quality=quality, method=6)
                    buffer.seek(0)
                    
                    base_name = os.path.splitext(os.path.basename(file_path))[0]
                    new_name = f"{base_name}.webp"
                    
                    image_field.save(new_name, ContentFile(buffer.read()), save=False)
                    obj.save(update_fields=[field_name])
                    
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    
                    converted += 1
            
            except Exception as e:
                messages.error(request, f"Ошибка при обработке {obj}: {str(e)}")
    
    if converted > 0:
        messages.success(request, f"Изображения успешно сжаты! Конвертировано: {converted}, пропущено: {skipped}.")
    elif skipped > 0:
        messages.info(request, f"Все изображения уже в WebP формате. Пропущено: {skipped}.")


compress_images_action.short_description = "Сжать изображения (WebP)"


@admin.register(WorkCase)
class WorkCaseAdmin(ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title',)
    actions = [compress_images_action]


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ('name', 'source', 'rating', 'date', 'order', 'is_approved', 'is_active')
    list_editable = ('order', 'is_approved', 'is_active')
    list_filter = ('source', 'rating', 'is_approved')
    search_fields = ('name', 'text')
