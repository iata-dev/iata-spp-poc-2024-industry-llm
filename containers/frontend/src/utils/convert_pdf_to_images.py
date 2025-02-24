from PIL import Image
import os
from pdf2image import convert_from_path

def convert_pdf_to_images(pdf_path):
    """Convert PDF to images and resize to a maximum of 1024x1024 while keeping the aspect ratio."""
    try:
        print(f'Converting PDF {pdf_path} to images...')
        images = convert_from_path(pdf_path, fmt='jpeg')
        image_paths = []
        for i, img in enumerate(images):
            img = img.convert('L')
            max_size = (920, 920)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            output_path = os.path.join(output_folder, f'{os.path.basename(pdf_path)}_page_{i}.jpg')
            img.save(output_path, 'JPEG', quality=30)
            image_paths.append(output_path)
        print(f'Converted and resized PDF to {len(images)} images.')
        return image_paths
    except Exception as e:
        print(f'Error converting PDF to images: {e}')
        return []

