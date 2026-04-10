"""
Import reviews from ReviewLab JSON into Django's Review model.
Run: python scratch/import_reviews.py
"""
import sys, io, os, json, django
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, '.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from portfolio.models import Review
from datetime import datetime, timezone

with open('scratch/all_reviews.json', 'r', encoding='utf-8') as f:
    reviews_data = json.load(f)

print(f"Loaded {len(reviews_data)} reviews from JSON")

# Map ReviewLab 'type' to a source label
SOURCE_MAP = {
    'googleMap': 'Google',
    'google': 'Google',
    '2gis': '2GIS',
    'twogis': '2GIS',
    'yandex': 'Яндекс',
}

created = 0
skipped = 0

for r in reviews_data:
    name = r.get('name', 'Аноним').strip()
    text = r.get('message', '').strip()
    rating = r.get('rating', 5)
    raw_date = r.get('date') or r.get('createdAt')
    review_type = r.get('type', 'googleMap')
    photo_url = r.get('photo', '')
    
    # Parse date
    review_date = None
    if raw_date:
        try:
            review_date = datetime.fromisoformat(raw_date.replace('Z', '+00:00')).date()
        except:
            pass
    
    # Determine source
    source = SOURCE_MAP.get(review_type, 'Google')
    
    # Skip if empty text and no rating info
    if not text and not name:
        skipped += 1
        continue
    
    # Use placeholder text if empty
    if not text:
        text = f'Отзыв от {name}'
    
    # Limit rating to 1-5
    rating = max(1, min(5, int(rating)))
    
    # Check for duplicate by name + text snippet
    text_snippet = text[:100]
    if Review.objects.filter(name=name, text__startswith=text_snippet).exists():
        skipped += 1
        continue
    
    review = Review.objects.create(
        name=name,
        text=text,
        rating=rating,
        source=source,
        source_url=r.get('src', ''),
        date=review_date,
        is_active=True,
        is_approved=True,
    )
    created += 1
    print(f"  Created: [{source}] {name} - {text[:60]}...")

print(f"\nDone! Created: {created}, Skipped: {skipped}")
print(f"Total reviews in DB: {Review.objects.count()}")
