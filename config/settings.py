"""
Django settings for config project.
"""

from pathlib import Path
import os
import dj_database_url
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-7srx_mhateiw+z$^#d5to7@rfkg4g&bjfu=f(+0&1b_ku44%&#')
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=lambda v: [s.strip() for s in v.split(',')])

if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.onrender.com']

INSTALLED_APPS = [
    'unfold',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'embed_video',
    'django_ckeditor_5',
    'core',
    'services',
    'leads',
    'portfolio',
    'blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Asia/Almaty'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# WhiteNoise Configuration (Aggressive Caching for Lighthouse 100/100)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_MAX_AGE = 31536000 # 1 year cache
WHITENOISE_KEEP_ONLY_HASHED_FILES = True

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─── Telegram Bot ──────────────────────────────────────────────────
TG_BOT_TOKEN = ''  # Вставьте токен бота от @BotFather
TG_CHAT_ID = ''    # Вставьте chat_id куда отправлять заявки


# ─── django-unfold ───────────────────────────────────────────────
UNFOLD = {
    "SITE_TITLE": "M-Clean Admin",
    "SITE_HEADER": "M-Clean",
    "SITE_SUBHEADER": "Панель управления",
    "STYLES": [
        lambda request: """
        #header [href='/admin/'] img { 
            max-height: 48px !important; 
            width: auto !important;
            flex-shrink: 0 !important;
        }
        #sidebar-nav .flex-shrink-0 { 
            flex-shrink: 0 !important;
        }
        """
    ],
    "COLORS": {
        "primary": {
            "50": "#ecfdf5",
            "100": "#d1fae5",
            "200": "#a7f3d0",
            "300": "#6ee7b7",
            "400": "#34d399",
            "500": "#10b981",
            "600": "#059669",
            "700": "#047857",
            "800": "#065f46",
            "900": "#064e3b",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "navigation": [
            {
                "title": "Управление",
                "separator": True,
                "items": [
                    {
                        "title": "Настройки",
                        "icon": "settings",
                        "link": "/admin/core/sitesettings/",
                    },
                ],
            },
            {
                "title": "Контент Главной",
                "separator": True,
                "items": [
                    {
                        "title": "Почему выбирают нас",
                        "icon": "star",
                        "link": "/admin/core/advantage/",
                    },
                    {
                        "title": "Как мы работаем",
                        "icon": "format_list_numbered",
                        "link": "/admin/core/workstep/",
                    },
                    {
                        "title": "Факты в цифрах",
                        "icon": "leaderboard",
                        "link": "/admin/core/companyfact/",
                    },
                ],
            },
            {
                "title": "Услуги",
                "separator": True,
                "items": [
                    {
                        "title": "Категории",
                        "icon": "category",
                        "link": "/admin/services/category/",
                    },
                    {
                        "title": "Услуги и цены",
                        "icon": "cleaning_services",
                        "link": "/admin/services/service/",
                    },
                    {
                        "title": "Доп. опции",
                        "icon": "add_circle",
                        "link": "/admin/services/additionaloption/",
                    },
                    {
                        "title": "Коэффициенты штор",
                        "icon": "straighten",
                        "link": "/admin/services/curtaincoefficient/",
                    },
                ],
            },
            {
                "title": "Контент",
                "separator": True,
                "items": [
                    {
                        "title": "Статьи блога",
                        "icon": "article",
                        "link": "/admin/blog/post/",
                    },
                    {
                        "title": "Категории блога",
                        "icon": "category",
                        "link": "/admin/blog/blogcategory/",
                    },
                    {
                        "title": "Портфолио (до/после)",
                        "icon": "photo_library",
                        "link": "/admin/portfolio/workcase/",
                    },
                    {
                        "title": "Отзывы",
                        "icon": "star",
                        "link": "/admin/portfolio/review/",
                    },
                    {
                        "title": "Партнёры",
                        "icon": "handshake",
                        "link": "/admin/core/partner/",
                    },
                    {
                        "title": "FAQ",
                        "icon": "help",
                        "link": "/admin/core/faq/",
                    },
                ],
            },
            {
                "title": "Акции и промо",
                "separator": True,
                "items": [
                    {
                        "title": "Акции и скидки",
                        "icon": "local_offer",
                        "link": "/admin/core/discount/",
                    },
                ],
            },
            {
                "title": "Технологии",
                "separator": True,
                "items": [
                    {
                        "title": "Оборудование",
                        "icon": "settings",
                        "link": "/admin/core/equipment/",
                    },
                    {
                        "title": "Чистящие средства",
                        "icon": "science",
                        "link": "/admin/core/chemical/",
                    },
                ],
            },
            {
                "title": "О компании",
                "separator": True,
                "items": [
                    {
                        "title": "Команда",
                        "icon": "group",
                        "link": "/admin/core/teammember/",
                    },
                    {
                        "title": "Сертификаты",
                        "icon": "workspace_premium",
                        "link": "/admin/core/certificate/",
                    },
                    {
                        "title": "Факты о нас",
                        "icon": "format_list_numbered",
                        "link": "/admin/core/companyfact/",
                    },
                ],
            },
            {
                "title": "Заявки",
                "separator": True,
                "items": [
                    {
                        "title": "Все заявки",
                        "icon": "mail",
                        "link": "/admin/leads/lead/",
                    },
                ],
            },
            {
                "title": "Обслуживание",
                "separator": True,
                "items": [
                    {
                        "title": "Оптимизация сайта",
                        "icon": "settings_backup_restore",
                        "link": "/admin/maintenance/",
                    },
                ],
            },
        ],
    },
}



# Django + YouTube
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# CSRF Trusted Origins for Render
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='http://localhost:8000,http://127.0.0.1:8000', cast=lambda v: [s.strip() for s in v.split(',')])
if '.onrender.com' not in str(CSRF_TRUSTED_ORIGINS):
    CSRF_TRUSTED_ORIGINS.append('https://*.onrender.com')

# ─── CKEditor 5 Configuration ─────────────────────────────────────
CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff" # User must be staff to upload

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                    'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],
    },
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|',
            'bulletedList', 'numberedList',
            '|',
            'blockQuote',
        ],
        'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
        'code','subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage',
                    'bulletedList', 'numberedList', 'todoList', '|',  'blockQuote', 'imageUpload', '|',
                    'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                    'insertTable',],
        'image': {
            'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
                        'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side',  '|'],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ]
        },
        'table': {
            'contentToolbar': [ 'tableColumn', 'tableRow', 'mergeTableCells',
            'tableProperties', 'tableCellProperties' ],
            'formatBlocks': [
                {
                    'name': 'Rows',
                    'classes': ['document-info']
                }
            ]
        },
        'heading' : {
            'options': [
                { 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },
                { 'model': 'heading1', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2' },
                { 'model': 'heading2', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3' }
            ]
        }
    }
}
