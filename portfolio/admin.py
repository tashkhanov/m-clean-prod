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
    list_display = ('title', 'category', 'order', 'is_active')
    list_editable = ('category', 'order', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('title',)
    actions = [compress_workcase_images]


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ('name', 'source', 'rating', 'date', 'order', 'is_approved', 'is_active')
    list_editable = ('order', 'is_approved', 'is_active')
    list_filter = ('source', 'rating', 'is_approved')
    search_fields = ('name', 'text')
