import json

from django.shortcuts import render, get_object_or_404

from core.models import SiteSettings
from blog.models import Post
from .models import Category, Service, AdditionalOption, CurtainCoefficient


def services_page(request):
    settings = SiteSettings.objects.first()
    categories = Category.objects.filter(is_active=True)
    services = Service.objects.filter(is_active=True)
    options = AdditionalOption.objects.filter(is_active=True)
    curtain_coeffs = CurtainCoefficient.objects.filter(is_active=True)

    # Собираем данные для калькулятора
    services_data = []
    for svc in services:
        svc_options = svc.options.filter(is_active=True)

        # Динамически формируем price_rules из ServiceTierPrice
        price_rules = None
        if svc.calc_type == 'carpet':
            tiers = svc.tiers.all().order_by('max_area')
            if tiers.exists():
                price_rules = {
                    'tiers': [
                        {'max_area': t.max_area, 'price': float(t.price)}
                        for t in tiers
                    ]
                }

        services_data.append({
            'id': svc.id,
            'name': svc.name,
            'slug': svc.slug,
            'calc_type': svc.calc_type,
            'base_price': float(svc.base_price),
            'premium_price': float(svc.premium_price),
            'unit': svc.unit,
            'icon': svc.icon,
            'price_rules': price_rules,
            'options': [
                {
                    'id': opt.id,
                    'name': opt.name,
                    'price': float(opt.price),
                    'calc_unit': opt.calc_unit,
                }
                for opt in svc_options
            ],
        })

    all_options_data = [
        {
            'id': opt.id,
            'name': opt.name,
            'price': float(opt.price),
            'calc_unit': opt.calc_unit,
            'services': list(opt.services.values_list('id', flat=True)),
        }
        for opt in options
    ]

    curtain_coeffs_data = [
        {'name': cc.name, 'coefficient': float(cc.coefficient)}
        for cc in curtain_coeffs
    ]

    # Минимальный заказ из настроек или по умолчанию
    min_order = int(settings.min_order) if settings and settings.min_order else 7000

    context = {
        'settings': settings,
        'categories': categories,
        'services': services,
        'options': options,
        'services_data': services_data,
        'all_options_data': all_options_data,
        'curtain_coeffs': curtain_coeffs_data,  # для шаблона
        'curtain_coeffs_data': json.dumps(curtain_coeffs_data, ensure_ascii=False),  # для JS
        'min_order': min_order,
        'categories_data': json.dumps(
            [{'id': c.id, 'name': c.name} for c in categories],
            ensure_ascii=False
        ),
    }

    return render(request, 'services/services.html', context)


def service_detail(request, slug):
    """Детальная страница услуги."""
    import json
    from portfolio.models import Review
    from django.db.models import Avg, Count
    
    settings = SiteSettings.objects.first()
    service = get_object_or_404(Service, slug=slug, is_active=True)
    options = AdditionalOption.objects.filter(is_active=True, services=service)
    all_options = AdditionalOption.objects.filter(is_active=True)
    curtain_coeffs = CurtainCoefficient.objects.filter(is_active=True)

    # Related blog posts (3 last)
    blog_posts = Post.objects.filter(is_published=True)[:3]

    # Review statistics
    reviews_qs = Review.objects.filter(is_active=True)
    review_stats = reviews_qs.aggregate(
        avg_rating=Avg('rating'),
        total_count=Count('id')
    )
    avg_rating = review_stats['avg_rating'] or 0
    review_count = review_stats['total_count'] or 0
    avg_rating_rounded = round(avg_rating, 1)

    # Steps for process timeline
    steps = [
        {'icon': 'phone', 'title': 'Заявка', 'description': 'Оставьте заявку на сайте или позвоните нам'},
        {'icon': 'calculator', 'title': 'Консультация и расчёт', 'description': 'Менеджер рассчитает стоимость и ответит на вопросы'},
        {'icon': 'calendar', 'title': 'Согласование времени', 'description': 'Выберите удобное время для выезда мастера'},
        {'icon': 'truck', 'title': 'Выезд мастера', 'description': 'Мастер приедет вовремя со всем необходимым оборудованием'},
        {'icon': 'sparkles', 'title': 'Проведение работ', 'description': 'Профессиональная чистка с гарантией результата'},
        {'icon': 'check-circle', 'title': 'Сдача и оплата', 'description': 'Вы проверяете результат и оплачиваете работу'},
    ]

    # JSON data for calculator
    all_options_data = [
        {
            'id': opt.id,
            'name': opt.name,
            'price': float(opt.price),
            'calc_unit': opt.calc_unit,
            'services': list(opt.services.values_list('id', flat=True)),
        }
        for opt in all_options
    ]

    curtain_coeffs_data = [
        {'name': cc.name, 'coefficient': float(cc.coefficient)}
        for cc in curtain_coeffs
    ]

    min_order = int(settings.min_order) if settings and settings.min_order else 7000

    # Build service JSON for single service page (Python dict for json_script)
    tiers = list(service.tiers.values('max_area', 'price').order_by('max_area'))
    price_rules = {'tiers': [{'max_area': t['max_area'], 'price': float(t['price'])} for t in tiers]} if tiers else None

    service_for_json = {
        'id': service.id,
        'name': service.name,
        'calc_type': service.calc_type,
        'base_price': float(service.base_price),
        'price_rules': price_rules,
    }

    context = {
        'settings': settings,
        'service': service,
        'options': options,
        'all_options': all_options,
        'blog_posts': blog_posts,
        'steps': steps,
        'avg_rating': avg_rating_rounded,
        'review_count': review_count,
        'all_options_data': all_options_data,  # Python list (json_script handles serialization)
        'curtain_coeffs_data': curtain_coeffs_data,  # Python list
        'curtain_coeffs': curtain_coeffs_data,  # for template loop
        'min_order': min_order,
        'service_for_json': service_for_json,
    }

    return render(request, 'services/service_detail.html', context)
