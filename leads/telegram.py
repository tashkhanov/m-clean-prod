import requests
from django.conf import settings


def send_telegram_notification(lead):
    """Отправляет уведомление о новой заявке в Telegram."""
    from core.models import SiteSettings
    settings_obj = SiteSettings.objects.first()

    if not settings_obj:
        return False

    token = settings_obj.telegram_bot_token
    chat_id = settings_obj.telegram_chat_id

    if not token or not chat_id:
        print(f"DEBUG: Telegram notifications NOT sent. Bot Token or Chat ID is missing in Admin.")
        return False

    text = (
        f"🔥 *Новая заявка!*\n"
        f"\n"
        f"👤 Имя: {lead.name}\n"
        f"📞 Телефон: {lead.phone}\n"
    )

    if lead.service_name:
        text += f"🔧 Услуга: {lead.service_name}\n"

    if lead.options:
        text += f"➕ Доп. опции: {lead.options}\n"

    if lead.total_price:
        text += f"💰 Сумма: {lead.total_price} ₸\n"

    if lead.message:
        text += f"💬 Сообщение: {lead.message}\n"

    text += f"\n🕐 {lead.created_at:%d.%m.%Y %H:%M}"

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    try:
        response = requests.post(url, json={
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'Markdown',
        }, timeout=5)
        return response.status_code == 200
    except Exception:
        return False
