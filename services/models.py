from django.db import models
from embed_video.fields import EmbedVideoField
from django_ckeditor_5.fields import CKEditor5Field


class Category(models.Model):
    name = models.CharField("Название", max_length=150)
    slug = models.SlugField("URL-адрес", max_length=150, unique=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Отображать?", default=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории услуг"
        ordering = ['order', '-id']

    def __str__(self):
        return self.name


class Service(models.Model):
    ICON_CHOICES = [
        ('sofa', 'Диван'),
        ('carpet', 'Ковёр'),
        ('mattress', 'Матрас'),
        ('chair', 'Кресло / Стул'),
        ('curtain', 'Шторы / Гардины'),
        ('car', 'Автомобиль'),
    ]
    
    CALC_TYPE_CHOICES = [
        ('default', 'Стандартный (поштучно)'),
        ('furniture', 'Мебель (диваны/кресла)'),
        ('carpet', 'Ковролин (по м²)'),
        ('curtains', 'Шторы (по весу/окнам)'),
    ]

    CLIENT_TYPE_CHOICES = [
        ('home', 'Физлица (Дом)'),
        ('business', 'Бизнес (Офис)'),
    ]
    
    MATERIAL_CHOICES = [
        ('fabric', 'Ткань'),
        ('leather', 'Кожа'),
    ]

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория",
        related_name="services"
    )
    icon = models.CharField(
        "Иконка",
        max_length=20,
        choices=ICON_CHOICES,
        default='sofa'
    )
    calc_type = models.CharField(
        "Тип калькулятора",
        max_length=20,
        choices=CALC_TYPE_CHOICES,
        default='default',
        help_text="Выберите тип расчёта для этой услуги"
    )
    default_client_type = models.CharField(
        "Тип клиента по умолчанию",
        max_length=10,
        choices=CLIENT_TYPE_CHOICES,
        default='home',
        help_text="Для калькулятора мебели"
    )
    default_material = models.CharField(
        "Материал по умолчанию",
        max_length=10,
        choices=MATERIAL_CHOICES,
        default='fabric',
        help_text="Для калькулятора мебели"
    )
    name = models.CharField("Название", max_length=200)
    slug = models.SlugField("URL-адрес", max_length=200, unique=True)
    short_description = models.TextField(
        "Краткое описание", 
        blank=True, 
        help_text="Для карточек и превью (1-2 предложения)"
    )
    description = CKEditor5Field("Описание", config_name='extends', blank=True)
    base_price = models.DecimalField(
        "Базовая цена (от)",
        max_digits=10,
        decimal_places=0,
        default=0,
        help_text="Обычная чистка"
    )
    unit = models.CharField(
        "Единица измерения",
        max_length=30,
        default="шт",
        help_text="Например: шт, м², комплект"
    )
    image = models.ImageField(
        "Фото",
        upload_to="services/",
        blank=True
    )
    image_alt = models.CharField("Alt-текст фото", max_length=255, blank=True, help_text="Для SEO")
    video = EmbedVideoField(
        verbose_name="Видео (YouTube)",
        blank=True,
        null=True,
        help_text="Вставьте полную ссылку на YouTube видео"
    )
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Отображать?", default=True)

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ['order', '-id']

    def __str__(self):
        return self.name


class ServiceTierPrice(models.Model):
    """Ступенчатая цена для услуг (например, ковролин: до 25м² — 2000 ₸/м²)."""
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name="Услуга",
        related_name='tiers'
    )
    max_area = models.PositiveIntegerField(
        "До скольки м²",
        help_text="Максимальная площадь для этого тарифа. Например: 25"
    )
    price = models.DecimalField(
        "Цена за м² (₸)",
        max_digits=10,
        decimal_places=0,
        default=0
    )

    class Meta:
        verbose_name = "Ступень цены"
        verbose_name_plural = "Ступени цен"
        ordering = ['max_area']

    def __str__(self):
        return f"{self.service.name}: до {self.max_area} м² — {self.price} ₸/м²"


class AdditionalOption(models.Model):
    CALC_UNIT_CHOICES = [
        ('fixed', 'Фиксированная цена'),
        ('per_kg', 'За кг'),
        ('per_m2', 'За м²'),
        ('per_item', 'За штуку'),
        ('percentage', 'Процент от суммы'),
    ]
    
    name = models.CharField("Название", max_length=200)
    price = models.DecimalField(
        "Цена (₸ или %)",
        max_digits=10,
        decimal_places=0,
        default=0,
        help_text="Фиксированная цена, цена за единицу или процент"
    )
    calc_unit = models.CharField(
        "Единица расчёта",
        max_length=20,
        choices=CALC_UNIT_CHOICES,
        default='fixed',
        help_text="Как считается: фиксировано, за кг, за м², за штуку или процент"
    )
    services = models.ManyToManyField(
        Service,
        verbose_name="Доступна для услуг",
        related_name="options",
        blank=True
    )
    show_in_furniture = models.BooleanField("В калькуляторе Мебели", default=True)
    show_in_carpet = models.BooleanField("В калькуляторе Ковролина", default=True)
    show_in_curtains = models.BooleanField("В калькуляторе Штор", default=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Отображать?", default=True)

    class Meta:
        verbose_name = "Доп. опция"
        verbose_name_plural = "Доп. опции (калькулятор)"
        ordering = ['order', '-id']

    def __str__(self):
        if self.calc_unit == 'percentage':
            return f"{self.name} (+{self.price}%)"
        elif self.calc_unit == 'per_kg':
            return f"{self.name} (+{self.price} ₸/кг)"
        elif self.calc_unit == 'per_m2':
            return f"{self.name} (+{self.price} ₸/м²)"
        elif self.calc_unit == 'per_item':
            return f"{self.name} (+{self.price} ₸/шт)"
        return f"{self.name} (+{self.price} ₸)"


class CurtainCoefficient(models.Model):
    """Коэффициент веса для расчёта штор по окнам."""
    name = models.CharField("Тип ткани", max_length=100)
    coefficient = models.DecimalField(
        "Коэффициент веса (кг/м²)",
        max_digits=5,
        decimal_places=2,
        default=0.6,
        help_text="Сколько кг весит 1 м² ткани"
    )
    price_per_kg = models.DecimalField(
        "Цена за кг (₸)",
        max_digits=10,
        decimal_places=0,
        null=True,
        blank=True,
        help_text="Оставьте пустым чтобы использовать базовую цену услуги. Заполните для переопределения цены для данного типа ткани."
    )
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Отображать?", default=True)

    class Meta:
        verbose_name = "Коэффициент штор"
        verbose_name_plural = "Коэффициенты штор"
        ordering = ['order', '-id']

    def __str__(self):
        price_str = f" — {self.price_per_kg} ₸/кг" if self.price_per_kg else ""
        return f"{self.name} ({self.coefficient} кг/м²{price_str})"

