import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from bs4 import BeautifulSoup
import json, re

with open('scratch/scraped_reviews.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

print(f"Page length: {len(str(soup))} chars")

# Look for ReviewLab specific classes (rl- prefix)
rl_items = soup.select('[class*="rl-"]')
print(f"\nElements with 'rl-' in class: {len(rl_items)}")
for el in rl_items[:5]:
    print(f"  tag={el.name} class={el.get('class')}")

# Look for iframes
iframes = soup.find_all('iframe')
print(f"\nIframes: {len(iframes)}")
for ifr in iframes:
    print(f"  src={ifr.get('src', '')[:120]}")

# Look for scripts with review/author data
scripts = soup.find_all('script')
print(f"\nTotal scripts: {len(scripts)}")
for sc in scripts:
    src = sc.get('src', '')
    if 'reviewlab' in src or 'review' in src:
        print(f"  Review script: {src}")
    if sc.string:
        txt = sc.string
        if 'reviewlab' in txt.lower() or '"author"' in txt or '"text"' in txt or '"rating"' in txt:
            print(f"\nScript with review data (first 800 chars):")
            print(txt[:800])

# Search for JSON-LD review schemas
jsonld = soup.find_all('script', type='application/ld+json')
for j in jsonld:
    try:
        data = json.loads(j.string)
        if isinstance(data, dict) and 'review' in str(data).lower():
            print(f"\nJSON-LD with reviews:")
            print(str(data)[:1000])
    except:
        pass

# Direct text search for review content patterns
body_text = soup.get_text()
# Find mentions of stars/ratings
star_pattern = re.findall(r'.{0,50}[★⭐✓✔].{0,50}', body_text)
print(f"\nStar patterns found: {len(star_pattern)}")
for s in star_pattern[:5]:
    print(f"  {s.strip()[:100]}")
