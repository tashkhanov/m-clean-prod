from .utils import optimize_image_field

def compress_images_action(modeladmin, request, queryset, image_fields=None, quality=75):
    """
    Переиспользуемый admin action для конвертации изображений в WebP + Resize.
    """
    if image_fields is None:
        image_fields = ['image']
    
    converted = 0
    skipped = 0
    errors = 0
    
    for obj in queryset:
        for field_name in image_fields:
            try:
                if optimize_image_field(obj, field_name, quality=quality):
                    converted += 1
                else:
                    skipped += 1
            except Exception as e:
                errors += 1
                messages.warning(request, f'Ошибка при обработке {obj}: {str(e)}')
    
    # Итоговое сообщение
    if converted > 0:
        messages.success(request, f'Изображения успешно сжаты! Конвертировано: {converted}')
    if skipped > 0:
        messages.info(request, f'Пропущено (уже WebP или другой формат): {skipped}')
    if errors > 0:
        messages.error(request, f'Ошибок при обработке: {errors}')
    if converted == 0 and skipped == 0 and errors == 0:
        messages.warning(request, 'Не найдено изображений для обработки')


def make_compress_action(image_fields=None, quality=75, short_description=None):
    """
    Фабрика для создания action с заданными параметрами.
    
    Args:
        image_fields: список полей с изображениями
        quality: качество WebP
        short_description: описание действия в админке
    
    Returns:
        Функция-action для регистрации в ModelAdmin
    """
    def compress_action(modeladmin, request, queryset):
        compress_images_action(modeladmin, request, queryset, image_fields, quality)
    
    compress_action.short_description = short_description or 'Сжать изображения (WebP)'
    compress_action.allowed_permissions = ['change']
    
    return compress_action


# Готовые actions для разных моделей
compress_service_images = make_compress_action(
    image_fields=['image'],
    quality=75,
    short_description='Сжать изображения услуги (WebP)'
)

compress_workcase_images = make_compress_action(
    image_fields=['image_before', 'image_after'],
    quality=75,
    short_description='Сжать изображения работы (WebP)'
)

compress_partner_logos = make_compress_action(
    image_fields=['logo'],
    quality=80,
    short_description='Сжать логотип партнёра (WebP)'
)

compress_team_photos = make_compress_action(
    image_fields=['photo'],
    quality=75,
    short_description='Сжать фото сотрудника (WebP)'
)

compress_certificate_images = make_compress_action(
    image_fields=['image'],
    quality=75,
    short_description='Сжать изображение сертификата (WebP)'
)

compress_discount_images = make_compress_action(
    image_fields=['image'],
    quality=75,
    short_description='Сжать изображение акции (WebP)'
)

compress_equipment_photos = make_compress_action(
    image_fields=['photo'],
    quality=75,
    short_description='Сжать фото оборудования (WebP)'
)

compress_chemical_photos = make_compress_action(
    image_fields=['photo'],
    quality=75,
    short_description='Сжать фото средства (WebP)'
)

compress_category_images = make_compress_action(
    image_fields=['image'],
    quality=75,
    short_description='Сжать изображение категории (WebP)'
)

compress_blog_images = make_compress_action(
    image_fields=['image'],
    quality=75,
    short_description='Сжать изображение статьи (WebP)'
)

compress_site_images = make_compress_action(
    image_fields=['logo', 'logo_footer', 'favicon', 'hero_image'],
    quality=75,
    short_description='Сжать изображения сайта (WebP)'
)
