from django.db import models


class Lead(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В работе'),
        ('done', 'Завершена'),
    ]

    name = models.CharField("Имя", max_length=150)
    phone = models.CharField("Телефон", max_length=30)
    service_name = models.CharField(
        "Услуга",
        max_length=200,
        blank=True,
        help_text="Услуга из калькулятора"
    )
    total_price = models.CharField(
        "Сумма",
        max_length=50,
        blank=True,
        help_text="Итоговая сумма из калькулятора"
    )
    options = models.TextField(
        "Доп. опции",
        blank=True,
        help_text="Выбранные дополнительные опции"
    )
    source_page = models.CharField(
        "Источник",
        max_length=255,
        blank=True,
        null=True,
        help_text="Страница, с которой отправлена форма"
    )
    message = models.TextField("Сообщение", blank=True)
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )
    created_at = models.DateTimeField("Создана", auto_now_add=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.phone} ({self.get_status_display()})"
