def generate_unique_filename(base_name, extension):
    """Generate a unique filename using the current date and time."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    return f'{timestamp}.{extension}'
