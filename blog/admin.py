from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import BlogCategory, Post, Tag
from core.admin_actions import make_compress_action


compress_blog_images = make_compress_action(
    image_fields=['image'],
    quality=75,
    short_description='Сжать изображение статьи (WebP)'
)


@admin.register(BlogCategory)
class BlogCategoryAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ('title', 'category', 'author', 'published_at', 'views', 'is_published', 'order')
    list_editable = ('order', 'is_published')
    list_filter = ('category', 'author', 'is_published', 'published_at', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'excerpt')
    actions = [compress_blog_images]
    readonly_fields = ('views', 'published_at')
    filter_horizontal = ('tags', 'faqs')
    
    fieldsets = (
        ("Основное", {
            'fields': ('category', 'author', 'tags', 'title', 'slug', 'image', 'image_alt', 'excerpt', 'content'),
        }),
        ("FAQ", {
            'fields': ('faqs',),
        }),
        ("SEO", {
            'fields': ('seo_title', 'seo_description'),
            'classes': ('collapse',),
        }),
        ("Публикация и Аналитика", {
            'fields': ('is_published', 'published_at', 'order', 'views'),
        }),
    )
