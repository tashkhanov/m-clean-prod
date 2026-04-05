import os
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image

def optimize_image_field(obj, field_name, quality=75, max_dim=1920):
    """
    Универсальная утилита для оптимизации изображения в поле модели.
    - Конвертирует в WebP
    - Сжимает (quality)
    - Ресайзит если больше max_dim
    - Удаляет старый файл
    """
    image_field = getattr(obj, field_name, None)
    if not image_field:
        return False

    try:
        file_path = image_field.path
        file_ext = os.path.splitext(file_path)[1].lower()

        # Если уже WebP, проверяем нужно ли ресайзить (обычно нет, если уже прошли оптимизацию)
        # Но для надежности проверяем размер всегда
        
        with Image.open(file_path) as img:
            orig_w, orig_h = img.size
            needs_resize = orig_w > max_dim or orig_h > max_dim
            needs_conversion = file_ext != '.webp'

            if not needs_resize and not needs_conversion:
                return False

            # 1. Ресайз
            if needs_resize:
                if orig_w > orig_h:
                    new_w = max_dim
                    new_h = int(orig_h * (max_dim / orig_w))
                else:
                    new_h = max_dim
                    new_w = int(orig_w * (max_dim / orig_h))
                img = img.resize((new_w, new_h), Image.LANCZOS)

            # 2. Подготовка к сохранению
            if img.mode in ('RGBA', 'P', 'LA'):
                img = img.convert('RGB')

            # 3. Сохранение
            buffer = BytesIO()
            img.save(buffer, format='WEBP', quality=quality, method=6)
            buffer.seek(0)
            
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            new_name = f"{base_name}.webp"
            
            # Сохраняем (Django создаст новый файл)
            image_field.save(new_name, ContentFile(buffer.read()), save=False)
            obj.save(update_fields=[field_name])

            # 4. Удаляем старый файл если расширение изменилось или путь другой
            if os.path.exists(file_path) and file_path != image_field.path:
                os.remove(file_path)
            
            return True
    except Exception:
        return False
