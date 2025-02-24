def encode_image(image_path):
    """Encode an image as a base64 data URL."""
    try:
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        logger.error(f'Error encoding image {image_path}: {str(e)}')
        return None
