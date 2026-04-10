from .models import SiteSettings, Partner, CompanyFact, Advantage, WorkStep
from services.models import Category


def site_context(request):
    """Добавляет настройки сайта и категории услуг в контекст всех шаблонов."""
    facts = CompanyFact.objects.filter(is_active=True)
    
    # Получаем факты для промо-блоков
    clients_count = None
    experience_count = None
    
    for fact in facts:
        if fact.icon == 'users':
            clients_count = f"{fact.value:,}{fact.suffix}".replace(',', ' ')
        elif fact.icon == 'calendar':
            experience_count = f"{fact.value}{fact.suffix}"
    
    settings = SiteSettings.objects.first()
    if settings and settings.about_short and clients_count:
        settings.about_short = settings.about_short.replace('10 000', clients_count).replace('10000', clients_count)
    
    from services.models import Service
    
    return {
        'settings': settings,
        'all_services': Service.objects.filter(is_active=True),
        'nav_partners': Partner.objects.filter(is_active=True)[:5],
        'company_facts': facts,
        'global_advantages': Advantage.objects.filter(is_active=True),
        'global_work_steps': WorkStep.objects.filter(is_active=True),
        'clients_count': clients_count or '10 000+',
        'experience_count': experience_count or '8+',
    }
