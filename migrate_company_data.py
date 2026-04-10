import os
import django
from bs4 import BeautifulSoup
from django.core.files import File
from django.utils.text import slugify
import sys
import shutil

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Ensure console output handles UTF-8 (Cyrillic)
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from core.models import TeamMember, Partner, Chemical, Equipment, Certificate, CompanyFact, Discount

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OLD_MCLEAN_DIR = os.path.join(BASE_DIR, 'old_mclean')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

def get_local_img_path(wp_path):
    """Converts WP image URL to local file path in old_mclean."""
    if not wp_path:
        return None
    # Remove leading slash if present
    rel_path = wp_path.lstrip('/')
    # Handle cases where path might be full URL (unlikely but safe)
    if 'wp-content' in rel_path:
        rel_path = rel_path[rel_path.find('wp-content'):]
    
    full_path = os.path.join(OLD_MCLEAN_DIR, rel_path)
    if os.path.exists(full_path):
        return full_path
    
    # Try common variations (e.g. without query params)
    full_path = full_path.split('?')[0]
    if os.path.exists(full_path):
        return full_path
        
    return None

def migrate_team():
    print("Migrating Team Members...")
    html_path = os.path.join(OLD_MCLEAN_DIR, 'kompaniya', 'komanda', 'index.html')
    if not os.path.exists(html_path):
        print(f"File not found: {html_path}")
        return

    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Find testimonial widgets or image boxes
    members = soup.select('.elementor-widget-testimonial, .elementor-widget-image-box, .elementor-widget-premium-testimonial')
    for m in members:
        name_tag = m.select_one('.elementor-testimonial__name, .elementor-image-box-title, .premium-testimonial-name')
        if not name_tag:
            continue
        
        name = name_tag.text.strip()
        pos_tag = m.select_one('.elementor-testimonial__title, .elementor-image-box-description, .premium-testimonial-title')
        position_text = pos_tag.text.strip() if pos_tag else ""
        
        bio_tag = m.select_one('.elementor-testimonial__content, .premium-testimonial-text')
        bio = bio_tag.text.strip() if bio_tag else ""

        img_tag = m.select_one('img')
        img_src = None
        if img_tag:
            img_src = img_tag.get('data-lazy-src') or img_tag.get('data-src') or img_tag.get('src')
        
        # Map WP position to Django choice
        pos_choice = 'master'
        pos_lower = position_text.lower()
        if 'директор' in pos_lower or 'менеджер' in pos_lower:
            pos_choice = 'manager'
        elif 'технолог' in pos_lower:
            pos_choice = 'tech'
        elif 'водитель' in pos_lower:
            pos_choice = 'driver'
        elif 'админ' in pos_lower:
            pos_choice = 'admin'

        obj, created = TeamMember.objects.get_or_create(name=name, defaults={
            'position': pos_choice,
            'bio': bio,
            'is_active': True
        })

        if img_src:
            local_path = get_local_img_path(img_src)
            if local_path:
                with open(local_path, 'rb') as f_img:
                    obj.photo.save(os.path.basename(local_path), File(f_img), save=True)
        
        print(f"  {'Created' if created else 'Updated'}: {name}")

def migrate_partners():
    print("Migrating Partners...")
    html_path = os.path.join(OLD_MCLEAN_DIR, 'kompaniya', 'klienty', 'index.html')
    if not os.path.exists(html_path):
        print(f"File not found: {html_path}")
        return

    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Partners are in pp-album and elementor-image widgets
    albums = soup.select('.elementor-widget-pp-album, .elementor-image')
    import re
    
    # Regex to extract partner name from title
    name_regex = re.compile(r'(?:компании|ресторане|кофейне|магазине|офисе|студии|центре|клинике|группе|салоне|отеле|гостинице|банке|школе|университете|вузе|аптеке|университет)\s+(?:(?:ООО|ИП|АО|ТОО)\s+)?(?:«([^»]+)»|([A-ZА-Я][a-zA-Zа-яА-Я\s&-]+))', re.IGNORECASE)

    for i, album in enumerate(albums):
        title_attr = album.select_one('a[data-elementor-lightbox-title]')
        desc_title = title_attr.get('data-elementor-lightbox-title') if title_attr else ""
        
        img_tag = album.select_one('img')
        img_src = None
        if img_tag:
            img_src = img_tag.get('data-lazy-src') or img_tag.get('data-src') or img_tag.get('src')
        
        if not img_src:
            continue

        name = ""
        if desc_title:
            match = name_regex.search(desc_title)
            if match:
                name = match.group(1) or match.group(2)
            else:
                quote_match = re.search(r'«([^»]+)»', desc_title)
                if quote_match:
                    name = quote_match.group(1)
                else:
                    name = desc_title.split(' ')[-1] if len(desc_title.split(' ')) > 2 else desc_title
                    
        # If still no name, try alt text or generate a generic one
        if not name or len(name) < 2:
            alt = img_tag.get('alt', '')
            if alt and len(alt) > 2:
                name = alt
            else:
                name = f"Партнёр {i+1}"
                
        name = name.strip()[:150] # Model limit

        # Check for duplicates based on name (case-insensitive) or image filename
        local_path = get_local_img_path(img_src)
        
        # Don't create if name already exists
        if Partner.objects.filter(name__iexact=name).exists():
           continue

        obj, created = Partner.objects.get_or_create(name=name, defaults={'is_active': True, 'order': i})
        
        if local_path and created:
            with open(local_path, 'rb') as f_img:
                obj.logo.save(os.path.basename(local_path), File(f_img), save=True)
        
        print(f"  {'Created' if created else 'Updated'}: {name}")

def migrate_cta_items(html_path, model_class, label):
    print(f"Migrating {label}...")
    if not os.path.exists(html_path):
        print(f"File not found: {html_path}")
        return

    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    items = soup.select('.elementor-widget-call-to-action')
    for item in items:
        title_tag = item.select_one('.elementor-cta__title')
        if not title_tag:
            continue
        
        title = title_tag.text.strip()
        desc_tag = item.select_one('.elementor-cta__description')
        desc = desc_tag.text.strip() if desc_tag else ""
        
        # Get background image from style or data-bg
        img_src = None
        bg_div = item.select_one('.elementor-cta__bg')
        if bg_div:
            img_src = bg_div.get('data-bg')
            if not img_src and bg_div.get('style'):
                style = bg_div.get('style')
                if 'url(' in style:
                    img_src = style.split('url(')[1].split(')')[0].strip('\'"')

        obj, created = model_class.objects.get_or_create(name=title, defaults={
            'description': desc,
            'is_active': True
        })

        if img_src:
            local_path = get_local_img_path(img_src)
            if local_path:
                with open(local_path, 'rb') as f_img:
                    # Both models have photo field
                    obj.photo.save(os.path.basename(local_path), File(f_img), save=True)
        
        print(f"  {'Created' if created else 'Updated'}: {title}")

def migrate_certificates():
    print("Migrating Certificates...")
    html_path = os.path.join(OLD_MCLEAN_DIR, 'kompaniya', 'sertifikaty', 'index.html')
    if not os.path.exists(html_path):
        print(f"File not found: {html_path}")
        return

    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Try different gallery selectors
    items = soup.select('.gallery-item, .elementor-gallery-item, .elementor-image')
    for item in items:
        img_tag = item.select_one('img')
        if not img_tag:
            continue
            
        caption_tag = item.select_one('figcaption, .gallery-caption')
        title = caption_tag.text.strip() if caption_tag else (img_tag.get('alt') or img_tag.get('title') or "Certificate")
        
        # Limit title length for model field
        title = title[:200]
        
        img_src = img_tag.get('data-lazy-src') or img_tag.get('data-src') or img_tag.get('src')
        
        if not img_src:
            continue

        obj = Certificate.objects.filter(title=title, category='cert').first()
        created = False
        if not obj:
            obj = Certificate.objects.create(title=title, category='cert', is_active=True)
            created = True

        local_path = get_local_img_path(img_src)
        if local_path and created:
            with open(local_path, 'rb') as f_img:
                obj.image.save(os.path.basename(local_path), File(f_img), save=True)
        
        print(f"  {'Created' if created else 'Updated'}: {title}")

def migrate_facts():
    print("Migrating Company Facts...")
    html_path = os.path.join(OLD_MCLEAN_DIR, 'kompaniya', 'index.html')
    if not os.path.exists(html_path):
        print(f"File not found: {html_path}")
        return

    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Find the facts section (has pp-counter)
    counters = soup.select('.elementor-widget-pp-counter')
    # Legacy data has 4 counters
    fact_data = [
        {'label': 'лет опыта работы в сфере чистки мягкой мягкой и ковры', 'icon': 'calendar'},
        {'label': 'довольных частных и корпоративных заказчиков', 'icon': 'users'},
        {'label': 'почищенных диванов, стульев, кресел и матрасов', 'icon': 'sofa'},
        {'label': 'квадратных метров чистых ковровых покрытий', 'icon': 'ruler'},
    ]

    for i, counter in enumerate(counters):
        if i >= len(fact_data):
            break
            
        num_tag = counter.select_one('.pp-counter-number')
        if not num_tag:
            continue
            
        value_str = num_tag.get('data-to', '0')
        value = int(value_str)
        prefix = counter.select_one('.pp-counter-number-prefix')
        suffix_text = prefix.text.strip() if prefix else ""
        
        # The labels are in a separate widget-text-editor after the counter
        # Better to use hardcoded labels mapping or try to find them
        label = fact_data[i]['label']
        icon = fact_data[i]['icon']

        obj, created = CompanyFact.objects.update_or_create(
            icon=icon,
            defaults={
                'label': label,
                'value': value,
                'suffix': suffix_text,
                'order': i,
                'is_active': True
            }
        )
        print(f"  {'Created' if created else 'Updated'}: {label} ({value}{suffix_text})")

def migrate_discounts():
    print("Migrating Discounts...")
    html_path = os.path.join(OLD_MCLEAN_DIR, 'skidki', 'index.html')
    if not os.path.exists(html_path):
        print(f"File not found: {html_path}")
        return

    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Clean out previous incorrectly parsed discounts first
    Discount.objects.all().delete()
    
    # 1. Standard approach for the 6 actual discounts in the layout
    discount_columns = soup.select('.our-services-col-1, .our-services-col-2, .our-services-col-3')
    
    for i, col in enumerate(discount_columns):
        title_tag = col.select_one('.our-discounts-title .elementor-heading-title')
        if not title_tag:
            continue
            
        # Standardize title spacing/newlines
        title = title_tag.get_text(separator=' ', strip=True).replace('  ', ' ')
        
        desc_tag = col.select_one('.our-discounts-text .elementor-text-editor')
        # Preserve newlines in description by using get_text with a separator or innerHTML
        # We replace <br/> with newline
        for br in desc_tag.find_all("br"):
            br.replace_with("\n")
        desc = desc_tag.get_text(strip=True) if desc_tag else ""
        
        # Extract percentage from the script settings in the circular progress bar
        pct = 0
        container = col.select_one('.premium-progressbar-container')
        if container:
            settings_str = container.get('data-settings', '')
            import json
            try:
                # Data-settings is JSON string
                settings_json = json.loads(settings_str)
                val = settings_json.get('progress_length', '0')
                pct = int(val)
            except:
                pass
                
        # If title doesn't contain скидка, continue (sanity check)
        if "Скидка" not in title and len(title) < 10: 
            continue

        Discount.objects.get_or_create(
            title=title, 
            defaults={
                'description': desc, 
                'discount_percent': pct if pct > 0 else None,
                'is_active': True, 
                'order': i
            }
        )
        print(f"  Created Discount: {title} ({pct}%)")

def migrate_gratitude_letters():
    print("Migrating Gratitude Letters...")
    
    # Strategy 1: Search Certificates Page with better heuristic
    html_path = os.path.join(OLD_MCLEAN_DIR, 'kompaniya', 'sertifikaty', 'index.html')
    processed_files = set()
    
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        images = soup.select('img')
        for img in images:
            alt = img.get('alt', '').lower()
            title = img.get('title', '').lower()
            src = img.get('data-lazy-src') or img.get('data-src') or img.get('src')
            
            if not src: continue
            
            is_letter = any(k in alt or k in title for k in ['благод', 'пис', 'отзыв', 'letter', 'thanks'])
            if is_letter:
                name = img.get('alt') or img.get('title') or "Благодарственное письмо"
                local_path = get_local_img_path(src)
                if local_path and local_path not in processed_files:
                    obj, created = Certificate.objects.get_or_create(title=name[:200], defaults={'category': 'gratitude', 'is_active': True})
                    with open(local_path, 'rb') as f_img:
                        obj.image.save(os.path.basename(local_path), File(f_img), save=True)
                    processed_files.add(local_path)
                    print(f"  Created Letter from page: {name}")

    # Scan uploads directory for obvious letters
    import glob
    search_patterns = ['*blagod*', '*pismo*', '*letter*', '*scan-письмо*']
    count = 0
    for pattern in search_patterns:
        files = glob.glob(os.path.join(OLD_MCLEAN_DIR, 'wp-content', 'uploads', '**', pattern), recursive=True)
        for f_path in files:
            if os.path.isdir(f_path): continue
            if f_path.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')) and f_path not in processed_files:
                name = os.path.basename(f_path).split('.')[0].replace('-', ' ').title()
                
                # Check for uniqueness based on file path to prevent duplicates
                if not Certificate.objects.filter(image__contains=os.path.basename(f_path)).exists():
                    obj, created = Certificate.objects.get_or_create(title=name[:200], defaults={'category': 'gratitude', 'is_active': True})
                    if created:
                        with open(f_path, 'rb') as f_img:
                            obj.image.save(os.path.basename(f_path), File(f_img), save=True)
                        count += 1
                        print(f"  Created Letter from filesystem: {name}")
                processed_files.add(f_path)
    
    if count == 0:
        print("  Notice: No new gratitude letters discovered.")

def migrate_all():
    migrate_team()
    migrate_partners()
    migrate_cta_items(os.path.join(OLD_MCLEAN_DIR, 'kompaniya', 'chistyashchie-sredstva', 'index.html'), Chemical, "Chemicals")
    migrate_cta_items(os.path.join(OLD_MCLEAN_DIR, 'kompaniya', 'oborudovanie', 'index.html'), Equipment, "Equipment")
    migrate_certificates()
    migrate_facts()
    migrate_discounts()
    migrate_gratitude_letters()
    print("Migration completed!")

if __name__ == '__main__':
    migrate_all()
