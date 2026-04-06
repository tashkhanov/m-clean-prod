import os
import django
import sys
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.utils import process_image_content
from core.models import SiteSettings
from portfolio.models import WorkCase

def create_test_image(size=(1200, 800), color='blue', name='test.jpg'):
    file = BytesIO()
    image = Image.new('RGB', size, color)
    image.save(file, 'JPEG')
    file.name = name
    file.seek(0)
    return SimpleUploadedFile(name, file.read(), content_type='image/jpeg')

def test_dual_watermarking():
    print("--- Testing Dual Watermarking for Portfolio ---")
    
    # 1. Ensure SiteSettings with Watermark exists
    settings = SiteSettings.objects.first()
    if not settings:
        settings = SiteSettings.objects.create()
    
    # Create a white watermark
    wm_file = create_test_image(size=(400, 150), color='white', name='watermark.png')
    settings.watermark.save('watermark.png', wm_file)
    settings.save()
    
    # 2. Create a WorkCase instance
    case = WorkCase(title="Test Case")
    
    # Create two different images
    img_before = create_test_image(size=(1000, 600), color='red', name='before.jpg')
    img_after = create_test_image(size=(1000, 600), color='green', name='after.jpg')
    
    # Save fields (this triggers pre_save signals)
    case.image_before.save('before.jpg', img_before, save=False)
    case.image_after.save('after.jpg', img_after, save=False)
    
    # Trigger save to execute signals
    case.save()
    
    # 3. Verify results
    print(f"Processed before: {case.image_before.name}")
    print(f"Processed after: {case.image_after.name}")
    
    assert case.image_before.name.endswith('.webp'), "Before image not converted to WebP"
    assert case.image_after.name.endswith('.webp'), "After image not converted to WebP"
    
    # Open images to verify they are valid and check dimensions
    with Image.open(case.image_before.path) as img1:
        print(f"Before image size: {img1.size}")
        assert img1.format == 'WEBP'
        
    with Image.open(case.image_after.path) as img2:
        print(f"After image size: {img2.size}")
        assert img2.format == 'WEBP'

    print("SUCCESS: Both Portfolio images processed and converted!")

if __name__ == "__main__":
    test_dual_watermarking()
