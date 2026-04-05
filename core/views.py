from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import (
    SiteSettings, Faq, Partner, BeforeAfter, Service, 
    TeamMember, Certificate, ServicePackage, Equipment, 
    Chemical, Discount, CompanyFact
)
from portfolio.models import WorkCase, Review
from blog.models import Post
from .utils import optimize_image_field


def index(request):
    settings = SiteSettings.objects.first()

    context = {
        'settings': settings,
        'faqs': Faq.objects.filter(is_active=True),
        'partners': Partner.objects.filter(is_active=True),
        'works': WorkCase.objects.filter(is_active=True),
        'reviews': Review.objects.filter(is_active=True, is_approved=True),
        'services': Service.objects.filter(is_active=True),
        'equipment': Equipment.objects.filter(is_active=True)[:4],
        'chemicals': Chemical.objects.filter(is_active=True)[:4],
        'team': TeamMember.objects.filter(is_active=True)[:6],
        'blog_posts': Post.objects.filter(is_published=True)[:3],
    }

    return render(request, 'index.html', context)


def about(request):
    """Страница 'О компании'."""
    settings = SiteSettings.objects.first()

    context = {
        'settings': settings,
        'team': TeamMember.objects.filter(is_active=True),
        'certificates': Certificate.objects.filter(is_active=True),
        'partners': Partner.objects.filter(is_active=True),
        'equipment': Equipment.objects.filter(is_active=True),
        'chemicals': Chemical.objects.filter(is_active=True),
        'facts': CompanyFact.objects.filter(is_active=True),
    }

    return render(request, 'about.html', context)


def prices(request):
    """Страница прайс-листа."""
    from services.models import Category, Service as ServiceItem, AdditionalOption
    
    settings = SiteSettings.objects.first()
    categories = Category.objects.filter(is_active=True)
    services = ServiceItem.objects.filter(is_active=True)
    options = AdditionalOption.objects.filter(is_active=True)

    context = {
        'settings': settings,
        'categories': categories,
        'services': services,
        'options': options,
    }

    return render(request, 'core/prices.html', context)


def technology(request):
    """Страница технологии и оборудование."""
    settings = SiteSettings.objects.first()

    context = {
        'settings': settings,
        'equipment': Equipment.objects.filter(is_active=True),
        'chemicals': Chemical.objects.filter(is_active=True),
    }

    return render(request, 'core/technology.html', context)


def discounts(request):
    """Страница акций и скидок."""
    settings = SiteSettings.objects.first()

    context = {
        'settings': settings,
        'discounts': Discount.objects.filter(is_active=True),
    }

    return render(request, 'core/discounts.html', context)


def reviews(request):
    """Страница отзывов."""
    settings = SiteSettings.objects.first()
    all_reviews = Review.objects.filter(is_active=True, is_approved=True)
    
    # Пагинация
    page = request.GET.get('page', 1)
    paginator = Paginator(all_reviews, 9)
    reviews_page = paginator.get_page(page)
    
    # Средний рейтинг по источникам
    ratings = {}
    sources = [
        ('yandex', 'Яндекс'),
        ('2gis', '2ГИС'),
        ('google', 'Google'),
    ]
    
    for key, name in sources:
        # 1. Проверяем ручной ввод (настройки)
        manual = getattr(settings, f'rating_{key}', None)
        if manual:
            ratings[key] = float(manual)
        else:
            # 2. Иначе считаем среднее по БД
            source_reviews = all_reviews.filter(source=key)
            if source_reviews.exists():
                avg = sum(r.rating for r in source_reviews) / source_reviews.count()
                ratings[key] = round(float(avg), 1)
            else:
                ratings[key] = 5.0  # Дефолт если ничего нет

    context = {
        'settings': settings,
        'reviews': reviews_page,
        'ratings': ratings,
        'total_count': all_reviews.count(),
        'range_5': range(1, 6),
    }

    return render(request, 'core/reviews.html', context)


def load_more_reviews(request):
    """AJAX endpoint для подгрузки отзывов."""
    page = request.GET.get('page', 1)
    all_reviews = Review.objects.filter(is_active=True, is_approved=True)
    paginator = Paginator(all_reviews, 9)
    reviews_page = paginator.get_page(page)
    
    reviews_data = []
    for review in reviews_page:
        reviews_data.append({
            'name': review.name,
            'text': review.text,
            'rating': review.rating,
            'source': review.get_source_display(),
            'date': review.date.strftime('%d.%m.%Y'),
        })
    
    return JsonResponse({
        'reviews': reviews_data,
        'has_next': reviews_page.has_next(),
        'next_page': reviews_page.next_page_number() if reviews_page.has_next() else None,
    })


def portfolio(request):
    """Страница портфолио с фильтрами."""
    from services.models import Category
    
    settings = SiteSettings.objects.first()
    category_slug = request.GET.get('category', '')
    
    works = WorkCase.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'settings': settings,
        'works': works,
        'categories': categories,
        'active_category': category_slug,
    }
    
    return render(request, 'core/portfolio.html', context)


def partners(request):
    """Страница партнеров."""
    settings = SiteSettings.objects.first()
    
    context = {
        'settings': settings,
        'partners': Partner.objects.filter(is_active=True),
    }
    
    return render(request, 'core/partners.html', context)


def maintenance(request):
    """
    Страница обслуживания системы в админке.
    Поддерживает AJAX-действия для пошаговой оптимизации.
    """
    from django.contrib.admin.views.decorators import staff_member_required
    from django.core.cache import cache
    from django.conf import settings as django_settings
    import os
    import glob
    
    # Регистрация моделей и полей для обработки
    from services.models import Service, Category
    from portfolio.models import WorkCase
    from blog.models import Post
    
    MODELS_CONFIG = {
        'sitesettings': (SiteSettings, ['logo', 'logo_footer', 'favicon', 'hero_image']),
        'service': (Service, ['image']),
        'category': (Category, ['image']),
        'workcase': (WorkCase, ['image_before', 'image_after']),
        'teammember': (TeamMember, ['photo']),
        'certificate': (Certificate, ['image']),
        'discount': (Discount, ['image']),
        'equipment': (Equipment, ['photo']),
        'chemical': (Chemical, ['photo']),
        'post': (Post, ['image']),
    }

    @staff_member_required
    def inner(request):
        action = request.GET.get('action')
        
        # 1. AJAX: Сбор статистики
        if action == 'get_stats' and request.method == 'POST':
            stats = []
            for key, (model, fields) in MODELS_CONFIG.items():
                # Считаем сколько записей всего может требовать обработки
                # (Простая оценка по количеству объектов)
                count = model.objects.count()
                if count > 0:
                    stats.append({'id': key, 'name': model._meta.verbose_name, 'count': count})
            return JsonResponse({'stats': stats})

        # 2. AJAX: Оптимизация конкретной модели
        if action == 'optimize_model' and request.method == 'POST':
            model_key = request.POST.get('model_id')
            if model_key not in MODELS_CONFIG:
                return JsonResponse({'error': 'Unknown model'}, status=400)
            
            model, fields = MODELS_CONFIG[model_key]
            optimized_count = 0
            for obj in model.objects.all():
                for field in fields:
                    if optimize_image_field(obj, field):
                        optimized_count += 1
            
            return JsonResponse({'optimized': optimized_count})

        # 3. AJAX: Очистка кэша
        if action == 'clear_cache' and request.method == 'POST':
            cache.clear()
            return JsonResponse({'status': 'success'})

        # 4. AJAX: Очистка мусора (orphaned files)
        if action == 'clean_orphans' and request.method == 'POST':
            total_deleted = 0
            media_root = django_settings.MEDIA_ROOT
            if os.path.exists(media_root):
                # Собираем все файлы в папке media
                all_files = set()
                for ext in ['*.jpg', '*.jpeg', '*.png', '*.webp']:
                    all_files.update(glob.glob(os.path.join(media_root, '**', ext), recursive=True))
                
                # Собираем пути из БД
                db_files = set()
                for _, (model, fields) in MODELS_CONFIG.items():
                    for obj in model.objects.all():
                        for field_name in fields:
                            field = getattr(obj, field_name, None)
                            if field and hasattr(field, 'path'):
                                try:
                                    db_files.add(os.path.normpath(field.path))
                                except: pass
                
                # Файлы, которых нет в БД
                to_delete = all_files - db_files
                for fpath in to_delete:
                    try:
                        os.remove(fpath)
                        total_deleted += 1
                    except: pass
                    
            return JsonResponse({'deleted': total_deleted})

        # GET: Отображение базовой страницы
        context = {
            'title': 'Обслуживание системы',
            'models_count': len(MODELS_CONFIG),
            'leads_count': Lead.objects.count(),
        }
        return render(request, 'admin/maintenance.html', context)
    
    return inner(request)

