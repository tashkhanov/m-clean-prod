import os
import django
import shutil
from bs4 import BeautifulSoup
from django.core.files import File
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from portfolio.models import WorkCase
from services.models import Category

LEGACY_ROOT = Path('old_mclean')
MEDIA_ROOT = Path('media')
PORTFOLIO_BEFORE = MEDIA_ROOT / 'portfolio' / 'before'
PORTFOLIO_AFTER = MEDIA_ROOT / 'portfolio' / 'after'

# Mapping: Legacy folder name -> Django category slug
CATEGORY_MAPPING = {
    'divany': 'himchistka-divanov',
    'divany-2': 'himchistka-divanov',
    'divany-3': 'himchistka-divanov',
    'divany-4': 'himchistka-divanov',
    'kovry': 'himchistka-kovrov',
    'kresla': 'himchistka-kresel',
    'matrasy': 'himchistka-matrasov',
    'stulya': 'himchistka-stulyev',
    'kozhanaya-mebel': 'himchistka-kozhanoj-mebeli',
}

def clean_path(path):
    if not path:
        return None
    # Remove leading slash and handle URL decoding if necessary
    return path.lstrip('/')

import re

def sync_portfolio():
    print("Starting Portfolio Migration...")
    
    # Ensure media directories exist
    PORTFOLIO_BEFORE.mkdir(parents=True, exist_ok=True)
    PORTFOLIO_AFTER.mkdir(parents=True, exist_ok=True)

    counts = {cat: 0 for cat in CATEGORY_MAPPING.values()}

    for folder_name, slug in CATEGORY_MAPPING.items():
        folder_path = LEGACY_ROOT / 'portfolio' / folder_name
        if not folder_path.exists():
            print(f"Skipping missing folder: {folder_path}")
            continue

        # Find index file
        index_file = folder_path / 'index.html'
        is_php = False
        if not index_file.exists():
            index_file = folder_path / 'index.php'
            is_php = True
        
        if not index_file.exists():
            print(f"No index file found in {folder_name}")
            continue

        print(f"Processing {folder_name} -> {slug}")
        
        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            print(f"Category slug '{slug}' not found in Django. Skipping.")
            continue

        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')

        figures = soup.find_all('figure', class_='gallery-item')
        pairs = []
        # Prefer PHP array extraction for PHP files
        if is_php:
            image_paths = re.findall(r"['\"](/wp-content/.*?)['\"]", content)
            if image_paths:
                # Pair them up: 0-1, 2-3, ...
                for j in range(0, len(image_paths) - 1, 2):
                    pairs.append((image_paths[j], image_paths[j+1]))
        
        # If no pairs from PHP, try standard BeautifulSoup parsing
        if not pairs and figures:
            i = 0
            while i < len(figures):
                fig_before = figures[i]
                caption_before = fig_before.find('figcaption').get_text(strip=True).lower() if fig_before.find('figcaption') else ""
                
                if "до чистки" in caption_before:
                    if i + 1 < len(figures):
                        fig_after = figures[i+1]
                        caption_after = fig_after.find('figcaption').get_text(strip=True).lower() if fig_after.find('figcaption') else ""
                        
                        if "после чистки" in caption_after:
                            a_before = fig_before.find('a')
                            src_before = a_before.get('href') if a_before else fig_before.find('img').get('src')
                            
                            a_after = fig_after.find('a')
                            src_after = a_after.get('href') if a_after else fig_after.find('img').get('src')
                            
                            pairs.append((src_before, src_after))
                            i += 2
                            continue
                i += 1

        # Process found pairs
        for src_before, src_after in pairs:
            try:
                # Localize paths
                local_before = LEGACY_ROOT / clean_path(src_before)
                local_after = LEGACY_ROOT / clean_path(src_after)

                def resolve_image(path):
                    if path.exists():
                        return path
                    if str(path).endswith('.webp'):
                        no_webp = Path(str(path).replace('.webp', ''))
                        if no_webp.exists():
                            return no_webp
                    return None

                real_before = resolve_image(local_before)
                real_after = resolve_image(local_after)

                if real_before and real_after:
                    work_title = f"{category.name} #{counts[slug] + 1}"
                    filename_before = real_before.name
                    filename_after = real_after.name
                    
                    target_before = PORTFOLIO_BEFORE / filename_before
                    target_after = PORTFOLIO_AFTER / filename_after
                    
                    if not target_before.exists():
                        shutil.copy2(real_before, target_before)
                    if not target_after.exists():
                        shutil.copy2(real_after, target_after)

                    WorkCase.objects.get_or_create(
                        title=work_title,
                        category=category,
                        image_before=f"portfolio/before/{filename_before}",
                        image_after=f"portfolio/after/{filename_after}",
                    )
                    counts[slug] += 1
                else:
                    # Don't spam, but log missing
                    pass
            except Exception as e:
                print(f"Error processing pair: {e}")

    print("\nMigration Complete!")
    for slug, count in counts.items():
        print(f"- {slug}: {count} pairs migrated")

if __name__ == "__main__":
    sync_portfolio()
