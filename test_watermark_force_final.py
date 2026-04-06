import os
import sys
import django
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.apps import apps
from core.models import SiteSettings

def create_test_image(size=(1200, 800), color='blue', name='test.jpg'):
    file = BytesIO()
    image = Image.new('RGB', size, color)
    image.save(file, 'JPEG')
    file.name = name
    file.seek(0)
    return SimpleUploadedFile(name, file.read(), content_type='image/jpeg')

def test_watermark_force_final():
    print("--- Testing Forced Watermark on WebP (100px Margin) ---")
    
    # 1. Setup Watermark
    settings = SiteSettings.objects.first()
    if not settings: settings = SiteSettings.objects.create()
    wm_data = create_test_image(size=(100, 100), color='white', name='wm_final.png')
    settings.watermark.save('wm_final.png', wm_data)
    
    # 2. Get WorkCase model
    WorkCase = apps.get_model('portfolio', 'WorkCase')
    case = WorkCase.objects.create(title="Final Watermark Force Test")
    
    # Upload an ALREADY WEBP image
    buffer = BytesIO()
    Image.new('RGB', (800, 600), 'red').save(buffer, 'WEBP')
    buffer.name = 'already_final.webp'
    buffer.seek(0)
    case.image_before.save('already_final.webp', ContentFile(buffer.read()), save=True)
    
    print(f"Original: {case.image_before.name}")
    
    # Trigger optimization logic
    from core.utils import optimize_image_field
    
    settings = SiteSettings.objects.first()
    master_watermark = settings.watermark
    
    # Force optimize
    success = optimize_image_field(case, 'image_before', watermark_file=master_watermark)
    
    if success:
        print(f"Result: {case.image_before.name}")
        if os.path.exists(case.image_before.path):
            with Image.open(case.image_before.path) as img:
                print(f"Final Info: {img.format}, {img.size}")
        print("SUCCESS: WebP file was RE-PROCESSED and watermark margin is now 100px!")
    else:
        print("FAILURE: WebP file was skipped!")

if __name__ == "__main__":
    test_watermark_force_final()
