from django.db import models
from embed_video.fields import EmbedVideoField


class SEOMixin(models.Model):
    """Абстрактная модель с SEO-полями для наследования другими моделями."""
    meta_title = models.CharField(
        "SEO Title",
        max_length=255,
        blank=True,
        help_text="Заголовок для поисковиков (до 60 символов)"
    )
    meta_description = models.TextField(
        "SEO Description",
        blank=True,
        help_text="Описание для поисковиков (до 160 символов)"
    )
    og_image = models.ImageField(
        "OG-изображение",
        upload_to="seo/og/",
        blank=True,
        help_text="Изображение для превью в соцсетях"
    )

    class Meta:
        abstract = True


class SiteSettings(models.Model):
    """Синглтон настроек сайта — одна запись, управляется через админку."""

    # Логотипы
    logo = models.ImageField(
        "Логотип",
        upload_to="branding/",
        blank=True,
        help_text="Основной логотип (для хедера)"
    )
    logo_footer = models.ImageField(
        "Логотип для футера",
        upload_to="branding/",
        blank=True,
        help_text="Белый/светлый логотип для тёмного футера"
    )
    favicon = models.ImageField(
        "Favicon",
        upload_to="branding/",
        blank=True,
        help_text="Иконка сайта (PNG, 32x32)"
    )
    hero_image = models.ImageField(
        "Фото Hero (справа)",
        upload_to="branding/",
        blank=True,
        help_text="Главное фото справа на первом экране (рекомендуется 600x500)"
    )
    hero_title = models.TextField(
        "Заголовок Hero (H1)",
        blank=True,
        help_text="HTML-разрешён. Например: Профессиональная<br><span>химчистка мебели</span><br>в Алматы"
    )
    hero_subtitle = models.TextField(
        "Подзаголовок Hero",
        blank=True,
        help_text="Текст под заголовком. Например: Вернём вашей мебели первозданный вид за 2 часа."
    )

    # Компания
    company_name = models.CharField(
        "Название компании",
        max_length=100,
        default="M-Clean"
    )
    tagline = models.CharField(
        "Слоган",
        max_length=255,
        blank=True,
        help_text="Например: Профессиональная химчистка мебели в Алматы"
    )
    about_short = models.TextField(
        "Краткое описание",
        blank=True,
        help_text="2-3 предложения для блока 'О нас' на главной"
    )

    # Контакты
    phone = models.CharField("Телефон", max_length=30)
    phone_secondary = models.CharField(
        "Доп. телефон",
        max_length=30,
        blank=True
    )
    email = models.EmailField("Email", blank=True)
    address = models.CharField(
        "Адрес",
        max_length=255,
        blank=True,
        help_text="Город, улица"
    )
    working_hours = models.CharField(
        "Часы работы",
        max_length=100,
        blank=True,
        default="Пн-Вс: 9:00 — 21:00"
    )
    min_order = models.DecimalField(
        "Минимальный заказ (₸)",
        max_digits=10,
        decimal_places=0,
        default=7000,
        help_text="Минимальная сумма заказа для выезда мастера"
    )

    # Соцсети
    whatsapp_phone = models.CharField("Номер WhatsApp", max_length=20, blank=True, help_text="Только цифры, например 77075288004")
    telegram = models.URLField("Telegram", blank=True)
    instagram = models.URLField("Instagram", blank=True)
    vk = models.URLField("VK", blank=True)

    # Рейтинги и ссылки на отзывы
    rating_yandex = models.DecimalField("Рейтинг Яндекс", max_digits=2, decimal_places=1, default=5.0)
    rating_google = models.DecimalField("Рейтинг Google", max_digits=2, decimal_places=1, default=5.0)
    rating_2gis = models.DecimalField("Рейтинг 2ГИС", max_digits=2, decimal_places=1, default=5.0)
    
    url_reviews_yandex = models.URLField("Ссылка на отзывы Яндекс", blank=True)
    url_reviews_google = models.URLField("Ссылка на отзывы Google", blank=True)
    url_reviews_2gis = models.URLField("Ссылка на отзывы 2ГИС", blank=True)

    # Уведомления Telegram
    telegram_bot_token = models.CharField("Telegram Bot Token", max_length=100, blank=True)
    telegram_chat_id = models.CharField("Telegram Chat ID", max_length=50, blank=True)

    # SEO главной
    seo_title = models.CharField(
        "SEO Title Главной",
        max_length=255,
        blank=True,
        help_text="Например: Химчистка мебели в Алматы | M-Clean"
    )
    seo_description = models.TextField(
        "SEO Description",
        blank=True,
        help_text="Описание для поисковой выдачи (до 160 символов)"
    )
    
    # Ресурсы
    watermark = models.ImageField(
        "Водяной знак", 
        upload_to="settings/", 
        blank=True, 
        null=True,
        help_text="PNG с прозрачностью для наложения на фото портфолио"
    )

    # Видео
    video = EmbedVideoField(
        verbose_name="Видео (YouTube)",
        blank=True,
        null=True,
        help_text="Вставьте полную ссылку на YouTube видео"
    )

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

    def __str__(self):
        return "Основные настройки"


class Faq(models.Model):
    question = models.CharField("Вопрос", max_length=255)
    answer = models.TextField("Ответ")
    order = models.PositiveIntegerField(
        "Порядок",
        default=0,
        help_text="Чем меньше число, тем выше"
    )
    is_active = models.BooleanField("Отображать?", default=True)

    class Meta:
        verbose_name = "Вопрос FAQ"
        verbose_name_plural = "FAQ (Вопросы и ответы)"
        ordering = ['order', '-id']

    def __str__(self):
        return self.question


class Partner(models.Model):
    name = models.CharField(
        "Название",
        max_length=150,
        help_text="Для alt-тегов (SEO)"
    )
    logo = models.ImageField("Логотип", upload_to="partners/")
    logo_alt = models.CharField("Alt-текст логотипа", max_length=255, blank=True)
    url = models.URLField(
        "Сайт партнёра",
        blank=True,
        help_text="Ссылка при клике (необязательно)"
    )
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Отображать?", default=True)

    class Meta:
        verbose_name = "Партнёр"
        verbose_name_plural = "Партнёры (Карусель)"
        ordering = ['order', '-id']

    def __str__(self):
        return self.name


class BeforeAfter(models.Model):
    title = models.CharField(
        "Заголовок",
        max_length=150,
        help_text="Например: Химчистка углового дивана"
    )
    image_before = models.ImageField(
        "Фото ДО",
        upload_to="before_after/before/"
    )
    image_after = models.ImageField(
        "Фото ПОСЛЕ",
        upload_to="before_after/after/"
    )
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Отображать?", default=True)

    class Meta:
        verbose_name = "Работа До/После"
        verbose_name_plural = "Работы До/После"
        ordering = ['order', '-id']

    def __str__(self):
        return self.title


class Service(SEOMixin):
    """Услуга клининга."""
    ICON_CHOICES = [
        ('sofa', 'Диван'),
        ('carpet', 'Ковёр'),
        ('mattress', 'Матрас'),
        ('chair', 'Кресло / Стул'),
        ('curtain', 'Шторы / Гардины'),
        ('car', 'Автомобиль'),
    ]

    icon = models.CharField(
        "Иконка",
        max_length=20,
        choices=ICON_CHOICES,
        default='sofa',
        help_text="Выберите иконку для карточки"
    )
    title = models.CharField("Название услуги", max_length=150)
    slug = models.SlugField(
        "URL-адрес",
        max_length=150,
        unique=True,
        help_text="Латиница, без пробелов (например: himchistka-divanov)"
    )
    short_description = models.CharField(
        "Краткое описание",
        max_length=300,
        help_text="Для карточки на главной (1-2 предложения)"
    )
    description = models.TextField(
        "Полное описание",
        blank=True,
        help_text="Для детальной страницы услуги"
    )
    price_from = models.DecimalField(
        "Цена от (₸)",
        max_digits=10,
        decimal_places=0,
        default=0,
        help_text="Базовая цена для отображения"
    )
    image = models.ImageField(
        "Фото",
        upload_to="services/",
        blank=True,
        help_text="Изображение для карточки"
    )
    video_url = models.URLField(
        "YouTube видео",
        blank=True,
        help_text="Ссылка на YouTube видео процесса чистки"
    )
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Отображать?", default=True)

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ['order', '-id']

    def __str__(self):
        return self.title




class TeamMember(models.Model):
    """Член команды M-Clean."""
    POSITION_CHOICES = [
        ('manager', 'Менеджер'),
        ('tech', 'Технолог'),
        ('master', 'Мастер'),
        ('driver', 'Водитель'),
        ('admin', 'Администратор'),
    ]

    name = models.CharField("Имя", max_length=150)
    position = models.CharField(
        "Должность",
        max_length=20,
        choices=POSITION_CHOICES,
        default='master'
    )
    experience_years = models.PositiveSmallIntegerField(
        "Опыт (лет)",
        default=0,
        help_text="Стаж работы в компании"
    )
    photo = models.ImageField(
        "Фото",
        upload_to="team/",
        blank=True,
        help_text="Портретное фото"
    )
    photo_alt = models.CharField("Alt-текст фото", max_length=255, blank=True)
    bio = models.TextField(
        "О сотруднике",
        blank=True,
        max_length=500,
        help_text="Краткая биография / интересные факты"
    )
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Отображать?", default=True)

    class Meta:
        verbose_name = "Член команды"
        verbose_name_plural = "Команда"
        ordering = ['order', '-id']

    def __str__(self):
        return f"{self.name} — {self.get_position_display()}"


class Certificate(models.Model):
    """Сертификат / благодарственное письмо."""
    CAT_CHOICES = (
        ('cert', 'Сертификат'),
        ('gratitude', 'Благодарственное письмо'),
    )

    title = models.CharField(
        "Название",
        max_length=200,
        help_text="Например: Сертификат IICRC, Благодарность от ТОО..."
    )
    category = models.CharField(
        "Категория",
        max_length=20,
        choices=CAT_CHOICES,
        default='cert'
    )
    image = models.ImageField(
        "Изображение",
        upload_to="certificates/"
    )
    image_alt = models.CharField("Alt-текст изображения", max_length=255, blank=True)
    issued_by = models.CharField(
        "Кем выдан",
        max_length=200,
        blank=True
    )
    issued_date = models.DateField(
        "Дата выдачи",
        null=True,
        blank=True
    )
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Отображать?", default=True)

    class Meta:
        verbose_name = "Сертификат"
        verbose_name_plural = "Сертификаты"
        ordering = ['order', '-id']

    def __str__(self):
        return self.title


class ServicePackage(models.Model):
    """Тарифы услуг: Стандарт и Премиум."""
    TIER_CHOICES = [
        ('standard', 'Стандарт'),
        ('premium', 'Премиум'),
    ]

    service = models.ForeignKey(
        'Service',
        on_delete=models.CASCADE,
        related_name='packages',
        verbose_name="Услуга"
    )
    tier = models.CharField(
        "Тариф",
        max_length=20,
        choices=TIER_CHOICES,
        default='standard'
    )
    price = models.DecimalField(
        "Цена (₸)",
        max_digits=10,
        decimal_places=0,
        help_text="Стоимость за единицу"
    )
    unit = models.CharField(
        "Единица измерения",
        max_length=50,
        default="шт",
        help_text="шт, м², комплект"
    )
    features = models.TextField(
        "Что входит",
        blank=True,
        help_text="Каждое преимущество с новой строки"
    )

    class Meta:
        verbose_name = "Тариф услуги"
        verbose_name_plural = "Тарифы услуг"
        ordering = ['service', 'tier']
        unique_together = ['service', 'tier']

    def __str__(self):
        return f"{self.service.title} — {self.get_tier_display()}"


class Equipment(models.Model):
    """Оборудование для химчистки."""
    name = models.CharField("Название", max_length=200)
    brand = models.CharField("Бренд", max_length=100, blank=True)
    photo = models.ImageField("Фото", upload_to="equipment/", blank=True)
    photo_alt = models.CharField("Alt-текст фото", max_length=255, blank=True)
    description = models.TextField("Описание", blank=True)
    features = models.TextField(
        "Характеристики",
        blank=True,
        help_text="Каждая характеристика с новой строки"
    )
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Отображать?", default=True)

    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"
        ordering = ['order', '-id']

    def __str__(self):
        return f"{self.brand} {self.name}" if self.brand else self.name


class Chemical(models.Model):
    """Чистящие средства."""
    ECO_CHOICES = [
        ('eco', 'Экологически безопасно'),
        ('hypo', 'Гипоаллергенно'),
        ('safe', 'Безопасно для детей и животных'),
        ('professional', 'Профессиональное средство'),
    ]

    name = models.CharField("Название", max_length=200)
    brand = models.CharField("Бренд", max_length=100, blank=True)
    photo = models.ImageField("Фото", upload_to="chemicals/", blank=True)
    photo_alt = models.CharField("Alt-текст фото", max_length=255, blank=True)
    description = models.TextField("Описание", blank=True)
    eco_status = models.CharField(
        "Эко-статус",
        max_length=20,
        choices=ECO_CHOICES,
        default='professional'
    )
    is_active = models.BooleanField("Отображать?", default=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Чистящее средство"
        verbose_name_plural = "Чистящие средства"
        ordering = ['order', '-id']

    def __str__(self):
        return f"{self.brand} {self.name}" if self.brand else self.name


class Discount(models.Model):
    """Акции и скидки."""
    title = models.CharField("Заголовок акции", max_length=200)
    description = models.TextField("Описание")
    discount_percent = models.PositiveSmallIntegerField(
        "Скидка (%)",
        null=True,
        blank=True
    )
    discount_amount = models.DecimalField(
        "Скидка (₸)",
        max_digits=10,
        decimal_places=0,
        null=True,
        blank=True
    )
    image = models.ImageField("Изображение", upload_to="discounts/", blank=True)
    image_alt = models.CharField("Alt-текст изображения", max_length=255, blank=True)
    valid_until = models.DateField("Действует до", null=True, blank=True)
    is_active = models.BooleanField("Отображать?", default=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции и скидки"
        ordering = ['order', '-id']

    def __str__(self):
        return self.title


class CompanyFact(models.Model):
    """Факты о компании для анимированных счетчиков."""
    ICON_CHOICES = [
        ('calendar', 'Календарь (опыт)'),
        ('users', 'Люди (клиенты)'),
        ('sofa', 'Диван (мебель)'),
        ('ruler', 'Линейка (метры)'),
    ]
    
    label = models.CharField("Название", max_length=100, help_text="Например: Лет опыта")
    value = models.PositiveIntegerField("Значение", help_text="Число для анимации (8, 10000, 5000)")
    suffix = models.CharField("Суффикс", max_length=10, blank=True, help_text="+ или тыс.")
    icon = models.CharField("Иконка", max_length=20, choices=ICON_CHOICES, default='calendar')
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Отображать?", default=True)

    class Meta:
        verbose_name = "Факт о компании"
        verbose_name_plural = "Факты о компании (счетчики)"
        ordering = ['order', '-id']

    def __str__(self):
        return f"{self.value}{self.suffix} {self.label}"
