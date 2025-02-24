def extract_value(text, key):
    """Extract a value corresponding to a key from a raw text."""
    try:
        pattern = f'\\"{key}\\".*?:.*?\\"(.*?)\\"'
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else ''
    except Exception as e:
        logger.error(f'Error extracting {key}: {e}')
        return ''
