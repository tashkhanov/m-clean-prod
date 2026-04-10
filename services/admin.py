from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline, StackedInline

from .models import Category, Service, AdditionalOption, CurtainCoefficient, ServiceTierPrice
from core.admin_actions import make_compress_action


# Admin actions
compress_service_images = make_compress_action(
    image_fields=['image'],
    quality=75,
    short_description='Сжать изображение услуги (WebP)'
)

compress_category_images = make_compress_action(
    image_fields=['image'],
    quality=75,
    short_description='Сжать изображение категории (WebP)'
)


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    actions = [compress_category_images]


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ('name', 'category', 'calc_type', 'base_price', 'icon', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('category', 'is_active', 'icon', 'calc_type')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    actions = [compress_service_images]
    inlines = []
    fieldsets = (
        ('Об услуге', {
            'fields': ('category', 'icon', 'calc_type', 'default_client_type', 'default_material', 'name', 'slug', 'short_description', 'description', 'image', 'image_alt'),
        }),
        ("Цены", {
            'fields': ('base_price', 'unit'),
            'description': "Укажите базовую стоимость за единицу измерения."
        }),
        ("Видео", {
            'fields': ('video',),
            'classes': ('collapse',),
            'description': "Вставьте полную ссылку на YouTube видео"
        }),
        ("Отображение", {
            'fields': ('order', 'is_active'),
        }),
    )

    def get_inlines(self, request, obj=None):
        """Показываем ступени цен только для услуг типа 'carpet'."""
        if obj and obj.calc_type == 'carpet':
            return [ServiceTierPriceInline]
        return []


class ServiceTierPriceInline(TabularInline):
    model = ServiceTierPrice
    extra = 1
    fields = ('max_area', 'price')
    verbose_name = "Ступень цены"
    verbose_name_plural = "Ступени цен (для ковролина)"
    ordering = ('max_area',)


@admin.register(AdditionalOption)
class AdditionalOptionAdmin(ModelAdmin):
    list_display = ('name', 'price', 'calc_unit', 'order', 'is_active')
    list_editable = ('order', 'is_active', 'price', )
    filter_horizontal = ('services',)
    search_fields = ('name',)
    list_filter = ('calc_unit',)
    fieldsets = (
        ("Основное", {
            'fields': ('name', 'price', 'calc_unit'),
            'description': "Выберите единицу расчёта: Фиксированная цена, За кг, За м², За штуку, или Процент от суммы"
        }),
        ("Привязка к конкретным услугам", {
            'fields': ('services',),
            'description': "Для отображения на странице КОНКРЕТНОЙ услуги."
        }),
        ("Привязка к типам калькулятора (Вкладки)", {
            'fields': ('show_in_furniture', 'show_in_carpet', 'show_in_curtains'),
            'description': "Показывать опцию при выборе типа калькулятора на общей странице."
        }),
        ("Отображение", {
            'fields': ('order', 'is_active'),
        }),
    )


@admin.register(CurtainCoefficient)
class CurtainCoefficientAdmin(ModelAdmin):
    list_display = ('name', 'coefficient', 'price_per_kg', 'order', 'is_active')
    list_editable = ('order', 'is_active', 'coefficient', 'price_per_kg')
    search_fields = ('name',)
    fieldsets = (
        ("Основное", {
            'fields': ('name', 'coefficient', 'price_per_kg'),
            'description': "Коэффициент веса в кг/м². Например: Обычные шторы = 0.6, Блэкаут = 1.1, Тюль = 0.2. Цена за кг — переопределение базовой цены (необязательно)."
        }),
        ("Отображение", {
            'fields': ('order', 'is_active'),
        }),
    )


@admin.register(ServiceTierPrice)
class ServiceTierPriceAdmin(ModelAdmin):
    list_display = ('service', 'max_area', 'price')
    list_filter = ('service',)
    search_fields = ('service__name',)
