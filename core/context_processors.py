from .models import SiteSettings, Partner, CompanyFact
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
    
    return {
        'settings': SiteSettings.objects.first(),
        'service_categories': Category.objects.filter(is_active=True),
        'nav_partners': Partner.objects.filter(is_active=True)[:5],
        'company_facts': facts,
        'clients_count': clients_count or '10 000+',
        'experience_count': experience_count or '8+',
    }
