"""
Fetch ALL reviews from ReviewLab API using the discovered widget ID.
"""
import sys, io, json, requests
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

WIDGET_ID = '64c3eaa394cb1342667732cb'
BASE_URL = f'https://app.reviewlab.ru/api/v1/widgets/widget/{WIDGET_ID}/reviews/remote'

all_reviews = []
skip = 0
limit = 50

print(f"Fetching reviews from ReviewLab API (widget: {WIDGET_ID})...")

while True:
    url = f'{BASE_URL}?skip={skip}&limit={limit}'
    print(f"  GET {url}")
    resp = requests.get(url, timeout=15)
    if resp.status_code != 200:
        print(f"  Error: {resp.status_code}")
        break
    
    data = resp.json()
    
    # Dump full structure on first call
    if skip == 0:
        print(f"\nResponse structure keys: {list(data.keys()) if isinstance(data, dict) else type(data)}")
        print(f"Sample (first 800 chars):\n{str(data)[:800]}\n")
    
    # Extract reviews from response
    reviews = []
    if isinstance(data, list):
        reviews = data
    elif isinstance(data, dict):
        reviews = data.get('reviews', data.get('items', data.get('data', [])))
    
    if not reviews:
        print(f"  No reviews in batch, stopping.")
        break
    
    all_reviews.extend(reviews)
    print(f"  Got {len(reviews)} reviews (total: {len(all_reviews)})")
    
    if len(reviews) < limit:
        print("  Got fewer than limit - reached end.")
        break
    
    skip += limit

print(f"\nTotal reviews fetched: {len(all_reviews)}")

# Save all reviews
with open('scratch/all_reviews.json', 'w', encoding='utf-8') as f:
    json.dump(all_reviews, f, ensure_ascii=False, indent=2)
print("Saved to scratch/all_reviews.json")

# Print summary
for i, r in enumerate(all_reviews[:5]):
    print(f"\nReview {i+1}:")
    print(f"  Keys: {list(r.keys()) if isinstance(r, dict) else r}")
