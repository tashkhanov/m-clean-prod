import os
import re
import sys
import uuid
import shutil
from pathlib import Path

import django
import sys

# System encoding fix for Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils.text import slugify
from bs4 import BeautifulSoup
from services.models import Service, Category
from core.models import Service as CoreService
from django.conf import settings

SERVICE_ROOT = Path(settings.BASE_DIR) / 'old_mclean'
LEGACY_SERVICES = [
    'himchistka-divanov',
    'himchistka-myagkoj-mebeli',
    'himchistka-kozhanoj-mebeli',
    'himchistka-kovrolina',
    'himchistka-kovrolina-v-ofise',
    'himchistka-matrasov',
    'himchistka-ofisnoj-mebeli',
    'himchistka-shtor',
    'himchistka-kresel',
    'himchistka-stulyev',
    'himchistka-kovrov',
    'chistka-bilyardnogo-stola',
]

ICON_MAP = {
    'диван': 'sofa',
    'мягкой мебели': 'sofa',
    'кожаной мебели': 'sofa',
    'ковров': 'carpet',
    'ковролина': 'carpet',
    'матрасов': 'mattress',
    'офисной мебели': 'chair',
    'офисного ковролина': 'carpet',
    'стульев': 'chair',
    'штор': 'curtain',
    'кресел': 'chair',
    'бильярдного стола': 'carpet',
}

def run():
    print("Deleting old services in core and services app...")
    Service.objects.all().delete()
    CoreService.objects.all().delete()
    Category.objects.all().delete()
    print("Deleted.")

    processed = set()
    for folder in LEGACY_SERVICES:
        if folder in processed: continue
        processed.add(folder)

        path = SERVICE_ROOT / folder
        if not path.is_dir():
            print(f'Skipping missing folder {folder}')
            continue
        # Find main html file
        html_file = None
        for candidate in ['index.html', 'index.php', 'index1.html', 'index1.php']:
            candidate_path = path / candidate
            if candidate_path.is_file():
                html_file = candidate_path
                break
        if not html_file:
            print(f'No HTML file found in {folder}')
            continue
        with open(html_file, encoding='utf-8', errors='ignore') as f:
            soup = BeautifulSoup(f, 'html.parser')

        # 1. Price extraction BEFORE aggressive cleanup
        prices = []
        # Try specific price classes
        for price_tag in soup.select('.price_item_cost'):
            txt = price_tag.get_text(separator=' ', strip=True)
            digits = re.findall(r'\d+', txt)
            if digits:
                try:
                    # Join all digits - this handles "1 500", "1.500", "1,500"
                    val = int(''.join(digits))
                    if val >= 500: # Minimal reasonable price for service
                        prices.append(val)
                except ValueError:
                    continue
        
        # Try tables if no prices found in specific classes
        if not prices:
            for table in soup.find_all('table'):
                table_text = table.get_text().lower()
                # If table mentions currency or price words
                if any(x in table_text for x in ['цена', 'стоимость', 'тг', '₸', 'тенге']):
                    for tr in table.find_all('tr'):
                        cells = tr.find_all(['td', 'th'])
                        if len(cells) >= 2:
                            # Look at the last 1-2 cells for numbers
                            # But skip the header row if it's just headers
                            if any(x in tr.get_text().lower() for x in ['наименование', 'размер']):
                                continue

                            for cell in reversed(cells):
                                txt = cell.get_text(separator=' ', strip=True)
                                # Remove common non-price numbers like "10-12 футов"
                                if 'фут' in txt or 'см' in txt: continue
                                
                                digits = re.findall(r'\d+', txt)
                                if digits:
                                    try:
                                        val = int(''.join(digits))
                                        if val >= 500: # Prices are likely >= 500
                                            prices.append(val)
                                            break # Found price in this row
                                    except ValueError:
                                        continue
        
        if prices:
            price = min(prices)
        else:
            # Fallback to old regex on raw soup text
            price = 0
            price_text = soup.get_text(separator=' ')
            # Handle "от 5 000" or "5000 тг" with various spaces
            price_match = re.search(r'от\s*([\d\s \.,]+)', price_text)
            if not price_match:
                 price_match = re.search(r'([\d\s \.,]+)\s*(?:тг|₸|тенге|т\.)', price_text.lower())
            
            if price_match:
                try:
                    price_digits = re.findall(r'\d+', price_match.group(1))
                    if price_digits:
                        val = int(''.join(price_digits))
                        if val >= 500:
                            price = val
                except ValueError:
                    price = 0

        # Debug print
        print(f"Processed service: {folder} | Price: {price}")

        # 2. Cleanup soup for description - use specific selectors to avoid junk
        for tag_name in ['header', 'footer', 'nav', 'script', 'style', 'aside', 'noscript']:
            for tag in soup.find_all(tag_name):
                tag.decompose()
        
        # Remove common navigation containers by selector
        for selector in ['.ast-header-bar', '.ast-footer-bar', '#masthead', '#colophon', '.main-navigation', '.breadcrumb', '.menu-toggle', '.ast-mobile-menu-buttons']:
            for junk in soup.select(selector):
                junk.decompose()

        # Title
        title_tag = soup.find(['h1'])
        if not title_tag:
            title_tag = soup.find('title')
        title = title_tag.get_text(strip=True) if title_tag else folder.replace('himchistka-', '').replace('-', ' ').title()
        
        # Clean title: Remove site name suffixes, newlines and multiple spaces
        title = re.split(r'[|—–-]', title)[0].replace('\n', ' ').strip()
        title = re.sub(r'\s+', ' ', title).strip()

        if 'Magic Clean' in title:
            title = title.replace('Magic Clean', '').strip()

        # Description - find the most relevant container
        content_div = soup.find(class_='entry-content') or soup.find(class_='elementor-section-wrap') or soup.find('main') or soup.find('body')
        full_desc = ""
        if content_div:
            # Get text with newlines to preserve some structure
            temp_text = content_div.get_text(separator='\n', strip=True)
            
            # Clean up known junk patterns
            temp_text = re.sub(r'(?i)Главное меню.*?в \.\.\.', '', temp_text, flags=re.DOTALL)
            temp_text = re.sub(r'(?i)Переключатель меню', '', temp_text)
            temp_text = re.sub(r'(?i)Услуги\s+Навигация по сайту', '', temp_text)
            
            # Filter lines
            lines = temp_text.split('\n')
            cleaned_lines = []
            content_started = False
            for line in lines:
                l = line.strip()
                if not l: continue
                
                # Logic to find where real content starts
                if not content_started:
                    if title.lower() in l.lower() or len(l.split()) > 5:
                        content_started = True
                        if l.lower() == title.lower():
                            continue
                
                if content_started:
                    if l in ['Услуги', 'Наши работы', 'Отзывы', 'Контакты', 'О компании']:
                        continue
                    cleaned_lines.append(l)
            full_desc = '\n'.join(cleaned_lines)

        # Improved Short description (Summary for cards)
        short_desc = ''
        # Strategy 1: Use Meta Description
        meta_desc_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_desc_tag and meta_desc_tag.get('content'):
            short_desc = meta_desc_tag['content'].strip()
        
        # Strategy 2: Fallback to first few sentences of cleaned description
        if not short_desc and full_desc:
            temp_desc = full_desc.replace('\n', ' ').strip()
            # Split into sentences
            sentences = re.split(r'(?<=[.!?])\s+', temp_desc)
            if sentences:
                if len(sentences) >= 2:
                    short_desc = sentences[0] + ' ' + sentences[1]
                else:
                    short_desc = sentences[0]
            
        # Refine length (limit to 180-200 chars for clean design)
        if len(short_desc) > 200:
            short_desc = short_desc[:197].rsplit(' ', 1)[0] + '...'
        
        if not short_desc:
            short_desc = f"Профессиональная {title.lower()} в Алматы. Качественно, быстро, с гарантией."

        # Unit
        unit = 'шт'
        text_for_unit = soup.get_text().lower()
        if 'м2' in text_for_unit or 'кв.м' in text_for_unit or 'м²' in text_for_unit:
            unit = 'м²'
        elif 'комплект' in text_for_unit:
            unit = 'комплект'

        # Icon
        icon = 'sofa'
        for key, val in ICON_MAP.items():
            if key in title.lower():
                icon = val
                break
        
        calc_type = 'default'
        if icon in ['sofa', 'chair', 'mattress']:
            calc_type = 'furniture'
        elif icon == 'carpet':
            calc_type = 'carpet'
        elif icon == 'curtain':
            calc_type = 'curtains'

        # Image
        img_tag = soup.find('img', class_=lambda x: x and 'wp-image' in x)
        if not img_tag:
            picture = soup.find('picture')
            if picture:
                img_tag = picture.find('img')
        if not img_tag:
            img_tag = soup.find('img')
        
        image_path = None
        if img_tag:
            src = img_tag.get('src') or img_tag.get('data-lazy-src') or img_tag.get('data-src')
            if src:
                src = src.lstrip('/')
                img_src_path = (SERVICE_ROOT.parent / src).resolve()
                if img_src_path.is_file():
                    dest_dir = Path(settings.MEDIA_ROOT) / 'services'
                    dest_dir.mkdir(parents=True, exist_ok=True)
                    new_name = f"{uuid.uuid4().hex}{img_src_path.suffix}"
                    dest_path = dest_dir / new_name
                    shutil.copy2(img_src_path, dest_path)
                    image_path = f"services/{new_name}"

        # Video
        video_url = None
        iframe = soup.find('iframe')
        if iframe and iframe.get('src') and 'youtube' in iframe.get('src'):
            video_url = iframe['src']

        # Save Category
        category, _ = Category.objects.get_or_create(slug=slugify(folder)[:150], defaults={'name': title})

        # Save to Functional model (services app)
        service, created = Service.objects.update_or_create(
            slug=slugify(folder)[:200],
            defaults={
                'category': category,
                'icon': icon,
                'calc_type': calc_type,
                'default_client_type': 'home',
                'default_material': 'fabric',
                'name': title,
                'short_description': short_desc,
                'description': full_desc,
                'base_price': price,
                'unit': unit,
                'image': image_path,
                'video': video_url,
                'is_active': True,
            },
        )

        # Save to Marketing model (core app - homepage cards)
        CoreService.objects.update_or_create(
             slug=slugify(folder)[:150],
             defaults={
                 'title': title,
                 'icon': icon,
                 'short_description': short_desc,
                 'description': full_desc,
                 'price_from': price,
                 'image': image_path,
                 'video_url': video_url or '',
                 'is_active': True
             }
        )

        print(f"Processed service: {title} | Price: {price} | Icon: {icon}")

if __name__ == '__main__':
    run()
