from django.contrib import admin
from django.contrib import messages
from django.core.files.base import ContentFile
from unfold.admin import ModelAdmin
from PIL import Image
import os
from io import BytesIO

from .models import WorkCase, Review


from core.admin_actions import compress_workcase_images


@admin.register(WorkCase)
class WorkCaseAdmin(ModelAdmin):
    list_display = ('title', 'category', 'order', 'is_active', 'show_on_homepage')
    list_editable = ('category', 'order', 'is_active', 'show_on_homepage')
    list_filter = ('category', 'is_active', 'show_on_homepage')
    search_fields = ('title', 'description', 'partner__name')
    actions = [compress_workcase_images]
    fieldsets = (
        ("Основное", {
            'fields': ('category', 'partner', 'title', 'description'),
        }),
        ("Изображения", {
            'fields': ('image_before', 'image_before_alt', 'image_after', 'image_after_alt'),
        }),
        ("Отображение", {
            'fields': ('order', 'is_active', 'show_on_homepage'),
        }),
    )


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ('name', 'source', 'rating', 'date', 'order', 'is_approved', 'is_active')
    list_editable = ('order', 'is_approved', 'is_active')
    list_filter = ('source', 'rating', 'is_approved')
    search_fields = ('name', 'text')
