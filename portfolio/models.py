from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class WorkCase(models.Model):
    category = models.ForeignKey(
        'services.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Категория",
        related_name="work_cases"
    )
    partner = models.ForeignKey(
        'core.Partner',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Партнёр / Клиент",
        related_name="work_cases"
    )
    title = models.CharField("Заголовок", max_length=200)
    description = models.TextField("Описание", blank=True)
    image_before = models.ImageField("Фото ДО", upload_to="portfolio/before/")
    image_before_alt = models.CharField("Alt-текст фото ДО", max_length=255, blank=True)
    image_after = models.ImageField("Фото ПОСЛЕ", upload_to="portfolio/after/")
    image_after_alt = models.CharField("Alt-текст фото ПОСЛЕ", max_length=255, blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Отображать?", default=True)
    show_on_homepage = models.BooleanField("Показывать на главной?", default=False)

    class Meta:
        verbose_name = "Работа (До/После)"
        verbose_name_plural = "Портфолио (До/После)"
        ordering = ['order', '-id']

    def __str__(self):
        return self.title


class Review(models.Model):
    SOURCE_CHOICES = [
        ('yandex', 'Яндекс'),
        ('2gis', '2ГИС'),
        ('google', 'Google'),
        ('own', 'Свой сайт'),
    ]

    name = models.CharField("Имя клиента", max_length=150)
    text = models.TextField("Текст отзыва")
    rating = models.PositiveSmallIntegerField(
        "Оценка",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    source = models.CharField(
        "Источник",
        max_length=20,
        choices=SOURCE_CHOICES,
        default='yandex'
    )
    date = models.DateField("Дата отзыва")
    source_url = models.URLField("Ссылка на оригинал отзыва", blank=True, null=True)
    is_approved = models.BooleanField("Одобрено к показу", default=True)
    is_active = models.BooleanField("Отображать?", default=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['order', '-date']

    def __str__(self):
        return f"{self.name} ({self.get_source_display()})"
