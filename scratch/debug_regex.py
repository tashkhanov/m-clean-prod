import re
from pathlib import Path

content = """
$portfolio = [
	'/wp-content/uploads/2020/08/kovry-1101-1.jpg.webp',
	'/wp-content/uploads/2020/08/kovry-1102-1.jpg.webp',
	'/wp-content/uploads/2020/08/kovry-1001-1.jpg.webp',
	'/wp-content/uploads/2020/08/kovry-1002-1.jpg.webp',
];
"""

image_paths = re.findall(r"['\"](/wp-content/.*?)['\"]", content)
print(f"Found {len(image_paths)} image paths")
for p in image_paths:
    print(f" - {p}")
