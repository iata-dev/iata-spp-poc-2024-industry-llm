def convert_pdf_to_images(pdf_path):
    """Convert PDF to images and resize to a maximum of 1024x1024 while keeping the aspect ratio."""
    try:
        logger.info(f'Converting PDF {pdf_path} to images...')
        images = convert_from_path(pdf_path, fmt='jpeg')
        image_paths = []
        for i, img in enumerate(images):
            img = img.convert('L')
            max_size = (920, 920)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            unique_filename = generate_unique_filename(f'{os.path.basename(pdf_path)}_page_{i}', 'jpg')
            output_path = os.path.join(output_folder, unique_filename)
            img.save(output_path, 'JPEG', quality=30)
            image_paths.append(output_path)
        logger.info(f'Converted and resized PDF to {len(images)} images.')
        return image_paths
    except Exception as e:
        logger.error(f'Error converting PDF to images: {e}')
        return []
