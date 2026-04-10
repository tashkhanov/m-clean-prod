"""
link_partners_to_works.py — скрипт для привязки партнеров к работам в портфолио.

Так как в старом сайте не было прямой базы данных с привязкой,
этот скрипт предлагает два подхода:
1. Случайная привязка — равномерное распределение работ по категориям среди партнеров
   (для демонстрации функционала, пока данные не заведены вручную).
2. Интерактивная привязка — выводит работы по категориям и позволяет указать партнера.

Запуск: python link_partners_to_works.py [--random]
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from portfolio.models import WorkCase
from core.models import Partner


def link_random():
    """Равномерно распределяет работы между активными партнерами."""
    partners = list(Partner.objects.filter(is_active=True))
    works = list(WorkCase.objects.filter(partner__isnull=True, is_active=True))

    if not partners:
        print("Нет активных партнеров!")
        return
    if not works:
        print("Все работы уже привязаны к партнерам.")
        return

    updated = 0
    for i, work in enumerate(works):
        partner = partners[i % len(partners)]
        work.partner = partner
        work.save(update_fields=['partner'])
        print(f"  {work.title[:60]} -> {partner.name}")
        updated += 1

    print(f"\nGotovo! Privyazano {updated} rabot k {len(partners)} partneram.")


def link_interactive():
    """Интерактивная привязка работ к партнерам."""
    partners = list(Partner.objects.filter(is_active=True))
    works = list(WorkCase.objects.filter(partner__isnull=True, is_active=True))

    if not partners:
        print("Нет активных партнеров!")
        return

    print("\n=== ПАРТНЕРЫ ===")
    for i, p in enumerate(partners):
        print(f"  [{i+1}] {p.name}")

    print(f"\nРаботы без партнера: {len(works)}")
    for work in works:
        print(f"\n  Работа: {work.title} (категория: {work.category.name if work.category else 'нет'})")
        idx = input("  Введите номер партнера (Enter — пропустить): ").strip()
        if idx.isdigit():
            p_idx = int(idx) - 1
            if 0 <= p_idx < len(partners):
                work.partner = partners[p_idx]
                work.save(update_fields=['partner'])
                print(f"  ✓ Привязано к {partners[p_idx].name}")

    print("\nГотово!")


if __name__ == '__main__':
    if '--random' in sys.argv:
        print("Режим: случайная привязка...")
        link_random()
    else:
        print("Режим: интерактивная привязка...")
        print("(Используйте --random для автоматической привязки)")
        link_interactive()
