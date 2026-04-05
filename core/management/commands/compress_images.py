import os
import re
from io import BytesIO
from pathlib import Path

from django.core.management.base import BaseCommand
from PIL import Image
from django.db import connection


class Command(BaseCommand):
    help = 'Конвертирует все JPG/PNG изображения в WebP с качеством 75% (сканирует файловую систему)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--quality',
            type=int,
            default=75,
            help='Качество WebP (1-100, по умолчанию 75)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Показать что будет сделано, но не выполнять',
        )
        parser.add_argument(
            '--skip-backup',
            action='store_true',
            help='Не создавать резервные копии оригиналов',
        )

    def handle(self, *args, **options):
        quality = options['quality']
        dry_run = options['dry_run']
        skip_backup = options['skip_backup']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('РЕЖИМ ПРОСМОТРА (изменения не сохраняются)'))
        
        converted = 0
        skipped = 0
        errors = 0
        
        # Определяем папки для обработки
        base_path = Path(__file__).resolve().parent.parent.parent.parent  # Корень проекта
        folders_to_process = [
            base_path / 'media',
            base_path / 'static',
        ]
        
        self.stdout.write(f'\nИщу все картинки в папках: {", ".join(str(f) for f in folders_to_process)}\n')
        
        # Сканируем все файлы рекурсивно
        image_files = []
        supported_formats = {'.jpg', '.jpeg', '.png'}
        
        for folder in folders_to_process:
            if not folder.exists():
                self.stdout.write(f'Папка не существует: {folder}')
                continue
            
            self.stdout.write(f'Сканирую: {folder}')
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = Path(root) / file
                    if file_path.suffix.lower() in supported_formats:
                        image_files.append(file_path)
        
        self.stdout.write(f'Найдено картинок: {len(image_files)}\n')
        
        # Обрабатываем каждый файл
        for file_path in sorted(image_files):
            file_ext = file_path.suffix.lower()
            file_name = file_path.name
            relative_path = file_path.relative_to(base_path)
            
            try:
                if dry_run:
                    self.stdout.write(f'[DRY] Конвертировал бы: {relative_path}')
                    converted += 1
                    continue
                
                # Открываем и конвертируем
                with Image.open(file_path) as img:
                    # Конвертируем в RGB если нужно (для PNG с прозрачностью)
                    if img.mode in ('RGBA', 'P', 'LA'):
                        # Создаем белый фон
                        rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                        img = rgb_img
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Сохраняем в WebP
                    new_file_path = file_path.parent / (file_path.stem + '.webp')
                    img.save(new_file_path, format='WEBP', quality=quality, method=6)
                    
                    # Создаем резервную копию оригинала если нужно
                    if not skip_backup:
                        backup_path = file_path.parent / (file_path.stem + f'_backup{file_ext}')
                        os.rename(file_path, backup_path)
                    else:
                        os.remove(file_path)
                    
                    self.stdout.write(self.style.SUCCESS(f'✓ {relative_path} -> {new_file_path.name}'))
                    converted += 1
            
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Ошибка обработки {relative_path}: {str(e)}'))
                errors += 1
        
        # Обновляем ссылки в БД
        self.stdout.write(f'\nОбновляю ссылки в базе данных...')
        db_updates = self.update_database_references(base_path, dry_run)
        
        # Итог
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS(f'✓ Конвертировано файлов: {converted}'))
        if db_updates > 0:
            self.stdout.write(self.style.SUCCESS(f'✓ Обновлено ссылок в БД: {db_updates}'))
        if errors > 0:
            self.stdout.write(self.style.ERROR(f'✗ Ошибок: {errors}'))
        self.stdout.write('=' * 60)
    
    def update_database_references(self, base_path, dry_run):
        """Обновляет ссылки на картинки в базе данных"""
        updates = 0
        
        # Список таблиц и полей для сканирования
        tables_to_check = [
            ('core_sitesettings', ['logo', 'logo_footer', 'favicon', 'hero_image']),
            ('services_service', ['image']),
            ('portfolio_workcase', ['image_before', 'image_after']),
            ('core_teammember', ['photo']),
            ('core_certificate', ['image']),
            ('core_discount', ['image']),
            ('core_equipment', ['photo']),
            ('core_chemical', ['photo']),
            ('blog_post', ['image']),
        ]
        
        try:
            with connection.cursor() as cursor:
                for table_name, fields in tables_to_check:
                    for field in fields:
                        # Проверяем существует ли таблица
                        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
                        if not cursor.fetchone():
                            continue
                        
                        # Получаем все записи с этим полем
                        cursor.execute(f"SELECT id, {field} FROM {table_name} WHERE {field} IS NOT NULL AND {field} != ''")
                        rows = cursor.fetchall()
                        
                        for row_id, image_path in rows:
                            if not image_path:
                                continue
                            
                            # Заменяем расширение на webp
                            for old_ext in ['.jpg', '.jpeg', '.png']:
                                if image_path.lower().endswith(old_ext):
                                    new_path = image_path.rsplit('.', 1)[0] + '.webp'
                                    
                                    if not dry_run:
                                        cursor.execute(
                                            f"UPDATE {table_name} SET {field} = %s WHERE id = %s",
                                            [new_path, row_id]
                                        )
                                        updates += 1
                                    break
                
                if not dry_run:
                    connection.commit()
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Предупреждение при обновлении БД: {str(e)}'))
        
        return updates
