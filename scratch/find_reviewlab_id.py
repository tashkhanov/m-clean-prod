"""
The reviews on m-clean.kz are loaded by ReviewLab widget (app.reviewlab.ru).
This script finds the ReviewLab widget app_id from the page and queries their API directly.
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import re, requests, json
from bs4 import BeautifulSoup

# Step 1: Find the ReviewLab app ID from the page source
with open('scratch/scraped_reviews.html', 'r', encoding='utf-8') as f:
    html = f.read()

# also re-fetch fresh copy with requests to see <script> config blocks
resp = requests.get('https://m-clean.kz/otzyvy/', timeout=15)
raw_html = resp.text

soup = BeautifulSoup(raw_html, 'html.parser')

# Look for ReviewLab initialization
# Pattern: data-app-id="xxxx" or reviewlab init
app_id = None
for attr_name in ['data-app-id', 'data-id', 'data-widget-id']:
    els = soup.find_all(attrs={attr_name: True})
    for e in els:
        print(f"Found {attr_name}={e[attr_name]} on {e.name}")
        if app_id is None:
            app_id = e[attr_name]

# Search inside script tags for reviewlab config
for sc in soup.find_all('script'):
    txt = sc.string or ''
    src = sc.get('src', '')
    if 'reviewlab' in txt.lower() or 'reviewlab' in src.lower():
        print(f"Script src: {src}")
        # Look for app ID patterns
        matches = re.findall(r'["\']([a-f0-9-]{8,})["\']', txt)
        if matches:
            print(f"  Potential IDs: {matches[:5]}")
        matches2 = re.findall(r'appId["\s:=]+["\']([^"\']+)["\']', txt, re.IGNORECASE)
        if matches2:
            print(f"  AppIds: {matches2}")

# Search in raw HTML for reviewlab-specific patterns
patterns = [
    r'reviewlab[^"]*app_id[^"]*["\']([^"\']+)["\']',
    r'["\']app_id["\']\s*:\s*["\']([^"\']+)["\']',
    r'reviewlab\.ru[^"]*["\']([a-f0-9-]{8,})["\']',
    r'data-uuid=["\']([^"\']+)["\']',
]
for pat in patterns:
    found = re.findall(pat, raw_html, re.IGNORECASE)
    if found:
        print(f"Pattern '{pat[:40]}': {found[:3]}")

# Try to find inline JSON config for the widget
json_blocks = re.findall(r'\{[^{}]*reviewlab[^{}]*\}', raw_html, re.IGNORECASE)
for block in json_blocks[:3]:
    print(f"JSON block: {block[:300]}")

print("\nDone scanning for ReviewLab config.")
