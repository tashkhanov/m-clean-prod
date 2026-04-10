import os
import re
import sys
from decimal import Decimal

os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from django.core.management.base import BaseCommand

from services.models import Category, Service


class Command(BaseCommand):
    help = 'Импорт услуг из старого сайта'

    SERVICES_DATA = [
        {
            'name': 'Химчистка диванов',
            'slug': 'himchistka-divanov',
            'icon': 'sofa',
            'calc_type': 'furniture',
            'base_price': Decimal('10000'),
            'unit': 'шт',
            'description': 'Профессиональная химчистка диванов на дому в Алматы. Выезд специалистов со всем оборудованием.',
        },
        {
            'name': 'Химчистка матрасов',
            'slug': 'himchistka-matrasov',
            'icon': 'mattress',
            'calc_type': 'furniture',
            'base_price': Decimal('5000'),
            'unit': 'шт',
            'description': 'Химчистка матрасов любых размеров. Удаление пятен, запахов и аллергенов.',
        },
        {
            'name': 'Химчистка кресел',
            'slug': 'himchistka-kresel',
            'icon': 'chair',
            'calc_type': 'furniture',
            'base_price': Decimal('5000'),
            'unit': 'шт',
            'description': 'Профессиональная химчистка кресел и стульев. Быстро и качественно.',
        },
        {
            'name': 'Химчистка мягкой мебели',
            'slug': 'himchistka-myagkoj-mebeli',
            'icon': 'sofa',
            'calc_type': 'furniture',
            'base_price': Decimal('8000'),
            'unit': 'шт',
            'description': 'Химчистка любой мягкой мебели: диваны, кресла, пуфы, банкетки.',
        },
        {
            'name': 'Химчистка кожаной мебели',
            'slug': 'himchistka-kozhanoj-mebeli',
            'icon': 'sofa',
            'calc_type': 'furniture',
            'base_price': Decimal('12000'),
            'unit': 'шт',
            'description': 'Специальная химчистка для кожаных изделий. Очистка, кондиционирование и защита.',
        },
        {
            'name': 'Химчистка офисной мебели',
            'slug': 'himchistka-ofisnoj-mebeli',
            'icon': 'chair',
            'calc_type': 'furniture',
            'base_price': Decimal('3000'),
            'unit': 'шт',
            'description': 'Химчистка офисных кресел, стульев и мягкой мебели для бизнеса.',
        },
        {
            'name': 'Химчистка стульев',
            'slug': 'himchistka-stulyev',
            'icon': 'chair',
            'calc_type': 'furniture',
            'base_price': Decimal('1500'),
            'unit': 'шт',
            'description': 'Химчистка стульев любых типов: деревянные с мягким сиденьем, офисные, барные.',
        },
        {
            'name': 'Химчистка штор',
            'slug': 'himchistka-shtor',
            'icon': 'curtain',
            'calc_type': 'curtains',
            'base_price': Decimal('8000'),
            'unit': 'окно',
            'description': 'Химчистка штор и гардин на дому. Тюль, бархат, блэкаут и другие ткани.',
        },
        {
            'name': 'Химчистка ковров',
            'slug': 'himchistka-kovrov',
            'icon': 'carpet',
            'calc_type': 'carpet',
            'base_price': Decimal('1500'),
            'unit': 'м²',
            'description': 'Химчистка ковров и ковровых покрытий с выездом на дом.',
        },
        {
            'name': 'Химчистка ковролина',
            'slug': 'himchistka-kovrolina',
            'icon': 'carpet',
            'calc_type': 'carpet',
            'base_price': Decimal('1500'),
            'unit': 'м²',
            'description': 'Профессиональная химчистка ковролина в квартирах и домах.',
        },
        {
            'name': 'Химчистка ковролина в офисе',
            'slug': 'himchistka-kovrolina-v-ofise',
            'icon': 'carpet',
            'calc_type': 'carpet',
            'base_price': Decimal('2000'),
            'unit': 'м²',
            'description': 'Химчистка ковровых покрытий в офисах и коммерческих помещениях.',
        },
        {
            'name': 'Чистка бильярдного стола',
            'slug': 'chistka-bilyardnogo-stola',
            'icon': 'sofa',
            'calc_type': 'default',
            'base_price': Decimal('15000'),
            'unit': 'шт',
            'description': 'Профессиональная чистка бильярдного стола и прилегающих элементов.',
        },
        {
            'name': 'Удаление неприятных запахов',
            'slug': 'udalenie-neprijatnyh-zapahov',
            'icon': 'sofa',
            'calc_type': 'default',
            'base_price': Decimal('3000'),
            'unit': 'м²',
            'description': 'Удаление неприятных запахов из помещений: табачный дым, запах животных, сырость.',
        },
    ]

    def handle(self, *args, **options):
        category, created = Category.objects.get_or_create(
            slug='himchistka-mebeli',
            defaults={
                'name': 'Химчистка мебели',
                'order': 1,
                'is_active': True,
            }
        )
        if created:
            print(f'[CREATED] Category: {category.name}')
        else:
            print(f'[EXISTS] Category: {category.name}')

        for i, service_data in enumerate(self.SERVICES_DATA, 1):
            service, created = Service.objects.get_or_create(
                slug=service_data['slug'],
                defaults={
                    'category': category,
                    'name': service_data['name'],
                    'icon': service_data['icon'],
                    'calc_type': service_data['calc_type'],
                    'base_price': service_data['base_price'],
                    'unit': service_data['unit'],
                    'description': service_data['description'],
                    'order': i,
                    'is_active': True,
                }
            )
            if created:
                print(f'[CREATED] {service.name} ({service.base_price} KZT/{service.unit})')
            else:
                print(f'[EXISTS] {service.name}')

        count = Service.objects.count()
        print(f'\nTotal: {count} services in database.')
