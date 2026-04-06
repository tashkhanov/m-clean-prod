import os
import sys
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image

def crop_to_aspect_ratio(img, target_ratio=1.6):
    """
    Аккуратно обрезает изображение по центру до заданного соотношения сторон.
    target_ratio = width / height (1.6 для 16:10)
    """
    w, h = img.size
    current_ratio = w / h

    if current_ratio > target_ratio:
        # Слишком широкое -> обрезаем бока
        new_w = int(h * target_ratio)
        offset = (w - new_w) // 2
        img = img.crop((offset, 0, offset + new_w, h))
    elif current_ratio < target_ratio:
        # Слишком высокое -> обрезаем верх/низ
        new_h = int(w / target_ratio)
        offset = (h - new_h) // 2
        img = img.crop((0, offset, w, offset + new_h))
    
    return img

def process_image_content(image_file, watermark_file=None, quality=80, max_dim=1920, force_16_10=False):
    """
    Универсальная обработка изображения:
    - (Опционально) Умная обрезка до 16:10
    - Ресайз до 1920px
    - Наложение водяного знака в "Безопасную зону" (10% от краев)
    - Конвертация в WebP
    """
    try:
        # Открываем основное изображение
        img = Image.open(image_file)
        
        # Сохраняем формат/прозрачность (RGBA для наложения)
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            img = img.convert('RGBA')
        else:
            img = img.convert('RGB')

        # 1. УМНАЯ ОБРЕЗКА (если нужно для Портфолио)
        if force_16_10:
            img = crop_to_aspect_ratio(img, target_ratio=1.6)

        # 2. Ресайз (по ширине)
        w, h = img.size
        if w > max_dim:
            new_w = max_dim
            new_h = int(h * (max_dim / w))
            img = img.resize((new_w, new_h), Image.LANCZOS)
            w, h = new_w, new_h

        # 3. Наложение водяного знака
        if watermark_file:
            try:
                wm_handle = watermark_file
                if hasattr(watermark_file, 'file'):
                    wm_handle = watermark_file.file
                
                if hasattr(wm_handle, 'seek'):
                    wm_handle.seek(0)
                    
                with Image.open(wm_handle) as wm:
                    wm = wm.convert('RGBA')
                    
                    # МАСШТАБ: Логотип всегда 15% от ширины фото
                    wm_width = int(w * 0.15)
                    if wm_width < 100: wm_width = 100 
                    
                    wm_height = int(wm.size[1] * (wm_width / wm.size[0]))
                    wm = wm.resize((wm_width, wm_height), Image.LANCZOS)
                    
                    # Прозрачность 50%
                    r, g, b, a = wm.split()
                    a = a.point(lambda p: int(p * 0.5))
                    wm = Image.merge('RGBA', (r, g, b, a))
                    
                    # ПОЗИЦИЯ: SAFE ZONE (10% отступа)
                    margin_x = int(w * 0.10)
                    margin_y = int(h * 0.10)
                    
                    paste_x = max(0, w - wm_width - margin_x)
                    paste_y = max(0, h - wm_height - margin_y)
                    
                    img.paste(wm, (paste_x, paste_y), wm)
            except Exception as e:
                sys.stderr.write(f"[ERROR] Watermark Applying Error: {e}\n")

        # 4. Сохранение в WebP
        buffer = BytesIO()
        img.save(buffer, format='WEBP', quality=quality, method=6)
        buffer.seek(0)
        
        orig_name = os.path.basename(image_file.name)
        base_name = os.path.splitext(orig_name)[0]
        if base_name.lower().endswith('.webp'):
            base_name = base_name[:-5]
        new_name = f"{base_name}.webp"
        
        return ContentFile(buffer.read(), name=new_name)
        
    except Exception as e:
        sys.stderr.write(f"[ERROR] Process Image Error: {e}\n")
        return None


def optimize_image_field(obj, field_name, watermark_file=None, quality=80, max_dim=1920, force_16_10=False):
    """Оптимизирует конкретное поле изображения."""
    image_field = getattr(obj, field_name, None)
    if not image_field or not image_field.name:
        return False

    is_webp = image_field.name.lower().endswith('.webp')
    # Если просят водяной знак ИЛИ обрезку — обрабатываем даже WebP
    if is_webp and not watermark_file and not force_16_10:
        return False

    processed_file = process_image_content(
        image_field, 
        watermark_file=watermark_file,
        quality=quality, 
        max_dim=max_dim,
        force_16_10=force_16_10
    )

    if processed_file:
        old_path = image_field.path if image_field and hasattr(image_field, 'path') else None
        image_field.save(processed_file.name, processed_file, save=False)
        obj.save(update_fields=[field_name])

        if old_path and os.path.exists(old_path) and old_path != image_field.path:
            try:
                os.remove(old_path)
            except Exception:
                pass
        return True
    return False
