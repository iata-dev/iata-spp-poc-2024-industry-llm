def check_keys(key, value):
    if isinstance(value, dict):
        for subkey, subvalue in value.items():
            check_keys(f'{key}.{subkey}', subvalue)
    elif not value or 'error' in str(value).lower() or 'null' in str(value).lower():
        missing_optional.append(key)
