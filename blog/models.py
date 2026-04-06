from django.db import models
from django.contrib.auth.models import User


class BlogCategory(models.Model):
    name = models.CharField("Название", max_length=150)
    slug = models.SlugField("URL-адрес", max_length=150, unique=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Категория блога"
        verbose_name_plural = "Категории блога"
        ordering = ['order', '-id']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField("Название тега", max_length=100)
    slug = models.SlugField("URL-адрес", max_length=100, unique=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Post(models.Model):
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Категория",
        related_name="posts"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Автор",
        related_name="blog_posts"
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        verbose_name="Теги",
        related_name="posts"
    )
    faqs = models.ManyToManyField(
        'core.Faq',
        blank=True,
        verbose_name="Вопросы FAQ",
        related_name="blog_posts"
    )
    title = models.CharField("Заголовок", max_length=300)
    slug = models.SlugField("URL-адрес", max_length=300, unique=True)
    image = models.ImageField("Изображение", upload_to="blog/")
    excerpt = models.TextField(
        "Краткое описание",
        max_length=500,
        help_text="Для превью в списке статей"
    )
    content = models.TextField(
        "Текст статьи (HTML)",
        help_text="Основной контент. Поддерживается HTML."
    )
    published_at = models.DateTimeField("Дата публикации", auto_now_add=True)
    is_published = models.BooleanField("Опубликована?", default=True)
    views = models.PositiveIntegerField("Просмотры", default=0)
    order = models.PositiveIntegerField("Порядок", default=0)

    # SEO
    seo_title = models.CharField(
        "SEO Title",
        max_length=255,
        blank=True,
        help_text="Заголовок для поисковиков"
    )
    seo_description = models.TextField(
        "SEO Description",
        blank=True,
        help_text="Описание для поисковой выдачи"
    )

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Блог (Статьи)"
        ordering = ['-published_at']

    def __str__(self):
        return self.title
