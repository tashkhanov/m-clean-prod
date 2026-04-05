import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Lead
from .telegram import send_telegram_notification


@require_POST
def submit_lead(request):
    """AJAX-приём заявки из модалки."""
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()

        if not name or not phone:
            return JsonResponse(
                {'success': False, 'error': 'Заполните имя и телефон'},
                status=400
            )

        lead = Lead.objects.create(
            name=name,
            phone=phone,
            service_name=data.get('service_name', ''),
            total_price=data.get('total_price', ''),
            options=data.get('options', ''),
            message=data.get('message', ''),
        )

        send_telegram_notification(lead)

        return JsonResponse({'success': True})

    except (json.JSONDecodeError, Exception):
        return JsonResponse(
            {'success': False, 'error': 'Ошибка сервера'},
            status=500
        )
