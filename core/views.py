import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import cache
from django.conf import settings

from .models import (
    SiteSettings, Faq, Partner, BeforeAfter, Service, 
    TeamMember, Certificate, ServicePackage, Equipment, 
    Chemical, Discount, CompanyFact, LegalPage
)
from services.models import Service as ServicesService
from portfolio.models import WorkCase, Review
from blog.models import Post
from leads.models import Lead
from leads.telegram import send_telegram_notification
from django.db.models import Count, Q
from .utils import process_image_content


def index(request):
    settings = SiteSettings.objects.first()

    context = {
        'settings': settings,
        'faqs': Faq.objects.filter(is_active=True, services__isnull=True),
        'partners': Partner.objects.filter(is_active=True),
        'works': WorkCase.objects.select_related('category', 'partner').filter(is_active=True)[:6],
        'reviews': Review.objects.filter(is_active=True, is_approved=True),
        'services': ServicesService.objects.filter(is_active=True).order_by('order', '-id')[:6],
        'equipment': Equipment.objects.filter(is_active=True)[:4],
        'chemicals': Chemical.objects.filter(is_active=True)[:4],
        'team': TeamMember.objects.filter(is_active=True)[:6],
        'blog_posts': Post.objects.select_related('category', 'author').filter(is_published=True)[:3],
    }

    return render(request, 'index.html', context)


def about(request):
    """Страница 'О компании'."""
    settings = SiteSettings.objects.first()

    context = {
        'settings': settings,
        'team': TeamMember.objects.filter(is_active=True),
        'certificates': Certificate.objects.filter(is_active=True, category='gratitude'),
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
        'certificates': Certificate.objects.filter(is_active=True, category='cert'),
        'range_5': range(5),
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
    
    source_filter = request.GET.get('source', 'all')
    reviews_queryset = Review.objects.filter(is_active=True, is_approved=True)
    
    if source_filter != 'all':
        reviews_queryset = reviews_queryset.filter(source=source_filter)
    
    paginator = Paginator(reviews_queryset, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'settings': settings,
        'page_obj': page_obj,
        'reviews': page_obj,
        'total_count': Review.objects.filter(is_active=True, is_approved=True).count(),
        'google_count': Review.objects.filter(is_active=True, is_approved=True, source='google').count(),
        'twogis_count': Review.objects.filter(is_active=True, is_approved=True, source='2gis').count(),
        'yandex_count': Review.objects.filter(is_active=True, is_approved=True, source='yandex').count(),
        'current_source': source_filter,
        'range_5': range(5),
    }

    return render(request, 'core/reviews.html', context)


def portfolio(request):
    """Страница выбора категории портфолио."""
    from services.models import Category
    from django.db.models import Prefetch
    settings = SiteSettings.objects.first()
    
    # Берем только категории, в которых есть хотя бы одна активная работа
    works_prefetch = Prefetch('work_cases', queryset=WorkCase.objects.filter(is_active=True).order_by('-id'))
    categories = Category.objects.filter(is_active=True).annotate(
        works_count=Count('work_cases', filter=Q(work_cases__is_active=True))
    ).filter(works_count__gt=0).prefetch_related(works_prefetch)

    # Для каждой категории найдем обложку (из последней работы)
    for cat in categories:
        # Используем предзагруженные данные, чтобы избежать N+1 запросов
        prefetched_works = cat.work_cases.all()
        cat.cover_image = prefetched_works[0].image_after if prefetched_works else None

    context = {
        'settings': settings,
        'categories': categories,
    }

    return render(request, 'core/portfolio.html', context)


def portfolio_category(request, slug):
    """Страница работ конкретной категории с пагинацией."""
    from services.models import Category
    settings = SiteSettings.objects.first()
    category = get_object_or_404(Category, slug=slug, is_active=True)
    
    works_list = category.work_cases.select_related('partner').filter(is_active=True).order_by('order', '-id')
    
    paginator = Paginator(works_list, 12) # 12 работ на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'settings': settings,
        'category': category,
        'page_obj': page_obj,
        'works': page_obj, # Для совместимости с текущим циклом в шаблоне
    }

    return render(request, 'core/portfolio_category.html', context)


def partners(request):
    """Страница партнеров."""
    settings = SiteSettings.objects.first()
    partners = Partner.objects.filter(is_active=True)

    context = {
        'settings': settings,
        'partners': partners,
    }

    return render(request, 'core/partners.html', context)


def contacts(request):
    """Страница контактов и форма обратной связи."""
    settings = SiteSettings.objects.first()

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message', '')
        source_page = request.POST.get('source_page', '')

        if name and phone:
            lead = Lead.objects.create(
                name=name,
                phone=phone,
                message=message,
                service_name="Сообщение со страницы контактов",
                source_page=source_page
            )
            try:
                send_telegram_notification(lead)
            except Exception:
                pass
            
            messages.success(request, 'Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.')
            return redirect('core:contacts')

    context = {
        'settings': settings,
    }
    return render(request, 'core/contacts.html', context)


@staff_member_required
def maintenance(request):
    """Вьюшка обслуживания системы (оптимизация медиа и очистка)."""
    action = request.GET.get('action')
    
    if request.method == 'POST':
        if action == 'get_stats':
            from portfolio.models import WorkCase
            from services.models import Service
            from blog.models import Post
            from core.models import Certificate, TeamMember, Partner

            # Статистика моделей для обработки
            stats = [
                {'id': 'workcase', 'name': 'Портфолио (До/После)', 'count': WorkCase.objects.count()},
                {'id': 'service', 'name': 'Услуги', 'count': Service.objects.count()},
                {'id': 'post', 'name': 'Блог', 'count': Post.objects.count()},
                {'id': 'certificate', 'name': 'Сертификаты', 'count': Certificate.objects.count()},
                {'id': 'teammember', 'name': 'Команда', 'count': TeamMember.objects.count()},
                {'id': 'partner', 'name': 'Партнеры', 'count': Partner.objects.count()},
            ]
            return JsonResponse({'stats': stats})

        elif action == 'optimize_model':
            from portfolio.models import WorkCase
            from services.models import Service
            from blog.models import Post
            from core.models import Certificate, TeamMember, Partner

            model_id = request.POST.get('model_id')
            optimized_count = 0
            
            # Логика маппинга моделей и полей
            process_map = {
                'workcase': (WorkCase, ['image_before', 'image_after']),
                'service': (Service, ['image']),
                'post': (Post, ['image']),
                'certificate': (Certificate, ['image']),
                'teammember': (TeamMember, ['photo']),
                'partner': (Partner, ['logo']),
            }
            
            if model_id in process_map:
                model_class, fields = process_map[model_id]
                items = model_class.objects.all()
                site_settings = SiteSettings.objects.first()
                
                for item in items:
                    for field_name in fields:
                        field_file = getattr(item, field_name)
                        if field_file:
                            # Оптимизация (WebP, Ресайз)
                            # Параметр force_16_10 только для портфолио
                            force_ratio = (model_id == 'workcase')
                            success = process_image_content(field_file, site_settings, force_16_10=force_ratio)
                            if success:
                                optimized_count += 1
                
                # Сохраняем изменения (пути файлов обновляются в процессе)
                # В данном случае process_image_content модифицирует файл на диске
                pass 
                
            return JsonResponse({'optimized': optimized_count})

        elif action == 'clear_cache':
            cache.clear()
            return JsonResponse({'status': 'ok'})

        elif action == 'clean_orphans':
            # Заглушка для удаления мусора (в реальности требует обхода папок медиа)
            return JsonResponse({'deleted': 0})

    context = {
        'leads_count': Lead.objects.count(),
        'models_count': 5,
    }
    return render(request, 'admin/maintenance.html', context)


def load_more_reviews(request):
    """AJAX подгрузка отзывов."""
    page = request.GET.get('page', 2)
    all_reviews = Review.objects.filter(is_active=True, is_approved=True)
    paginator = Paginator(all_reviews, 12)
    
    try:
        reviews_page = paginator.page(page)
        data = []
        for r in reviews_page:
            data.append({
                'name': r.name,
                'text': r.text,
                'rating': r.rating,
                'source': r.source,
                'source_display': r.get_source_display(),
                'date': r.date.strftime('%d.%m.%Y'),
            })
        return JsonResponse({'reviews': data, 'has_next': reviews_page.has_next()})
    except Exception:
        return JsonResponse({'error': 'Page not found'}, status=404)

def partners_list(request):
    """Страница Наши партнеры."""
    settings = SiteSettings.objects.first()

    context = {
        'settings': settings,
        'partners': Partner.objects.filter(is_active=True),
    }

    return render(request, 'core/partners_list.html', context)


def get_partner_works(request, partner_id):
    """AJAX подгрузка работ партнера для модалки."""
    partner = get_object_or_404(Partner, id=partner_id, is_active=True)
    works = WorkCase.objects.filter(partner=partner, is_active=True)

    data = []
    for w in works:
        data.append({
            'title': w.title,
            'image_before': w.image_before.url if w.image_before else None,
            'image_after': w.image_after.url if w.image_after else None,
        })

    return JsonResponse({
        'partner_name': partner.name,
        'partner_logo': partner.logo.url if partner.logo else None,
        'partner_description': partner.description if hasattr(partner, 'description') else '',
        'works': data
    })


def legal_page_detail(request, slug):
    """Отображение динамической юридической страницы (Политика, Оферта)."""
    settings = SiteSettings.objects.first()
    page = get_object_or_404(LegalPage, slug=slug, is_active=True)
    
    context = {
        'settings': settings,
        'page': page,
    }
    return render(request, 'core/legal_page.html', context)


def notice_page(request):
    """Страница 'Уведомление о рисках' с аккордеонами."""
    settings = SiteSettings.objects.first()
    # Пытаемся получить контент из базы, если админ захочет поменять текст
    page = LegalPage.objects.filter(slug='notice', is_active=True).first()
    
    context = {
        'settings': settings,
        'page': page,
    }
    return render(request, 'core/notice.html', context)

