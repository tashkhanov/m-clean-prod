from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Lead


@admin.register(Lead)
class LeadAdmin(ModelAdmin):
    list_display = ('name', 'phone', 'service_name', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    list_editable = ('status',)
    search_fields = ('name', 'phone', 'service_name')
    list_per_page = 50
    readonly_fields = ('name', 'phone', 'service_name', 'total_price', 'options', 'message', 'source_page', 'discount_info', 'created_at')
    fieldsets = (
        ("Данные клиента", {
            'fields': ('name', 'phone', 'service_name', 'options', 'total_price', 'message'),
        }),
        ("Аналитика", {
            'fields': ('source_page', 'discount_info'),
        }),
        ("Статус", {
            'fields': ('status', 'created_at'),
        }),
    )

    def has_add_permission(self, request):
        return False
