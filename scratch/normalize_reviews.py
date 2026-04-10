"""
Normalize review sources and fix links.
Run: python scratch/normalize_reviews.py
"""
import sys, io, os, django
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, '.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from portfolio.models import Review

print("Normalizing review sources...")

# 1. Map existing capitalized sources to lowercase keys
# 2. Re-detect source from URL if possible

reviews = Review.objects.all()
google_count = 0
twogis_count = 0
yandex_count = 0
fixed_links = 0

for r in reviews:
    old_source = r.source
    url = r.source_url or ""
    
    # Set based on URL content (more reliable)
    if 'google.com' in url.lower():
        r.source = 'google'
    elif '2gis.kz' in url.lower() or '2gis.ru' in url.lower():
        r.source = '2gis'
    elif 'yandex.kz' in url.lower() or 'yandex.ru' in url.lower():
        r.source = 'yandex'
    else:
        # Fallback to normalized old source
        if old_source.lower() in ['google', 'googlemap']:
            r.source = 'google'
        elif old_source.lower() in ['2gis', 'twogis']:
            r.source = '2gis'
        elif old_source.lower() in ['yandex']:
            r.source = 'yandex'

    if r.source != old_source:
        r.save()
        print(f"  Updated source for '{r.name}': {old_source} -> {r.source}")

    if r.source == 'google': google_count += 1
    elif r.source == '2gis': twogis_count += 1
    elif r.source == 'yandex': yandex_count += 1

print(f"\nFinished normalization!")
print(f"  Google: {google_count}")
print(f"  2GIS: {twogis_count}")
print(f"  Yandex: {yandex_count}")
print(f"Total reviews in DB: {Review.objects.count()}")
