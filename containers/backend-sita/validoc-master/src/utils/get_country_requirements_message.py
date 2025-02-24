def get_country_requirements_message(exporting_country, importing_country, requirements):
    """
    Fetch and format export/import requirements for given countries.

    :param exporting_country: Alpha-2 code of the exporting country
    :param importing_country: Alpha-2 code of the importing country
    :param requirements: Parsed JSON data containing requirements
    :return: Formatted string with simplified requirements
    """
    all_requirements = requirements.get('requirements', {})
    exporting_data = all_requirements.get(exporting_country, {}).get('exporting', [])
    importing_data = all_requirements.get(importing_country, {}).get('importing', [])
    exporting_message = f"Requirements for Exporting from {exporting_country or 'Unknown'}:\n"
    if exporting_data:
        exporting_message += '\n'.join(exporting_data) + '\n'
    else:
        exporting_message += 'None found\n'
    importing_message = f"\nRequirements for Importing to {importing_country or 'Unknown'}:\n"
    if importing_data:
        importing_message += '\n'.join(importing_data) + '\n'
    else:
        importing_message += 'None found\n'
    return exporting_message + importing_message
