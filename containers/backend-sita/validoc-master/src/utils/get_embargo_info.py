def get_embargo_info(importing_country, embargo_data):
    """
    Fetch embargo restrictions for a given importing country.
    
    :param importing_country: Alpha-2 code of the importing country
    :param embargo_data: List of embargoed countries with restrictions
    :return: Restrictions if the country is under embargo, otherwise None
    """
    for embargo_entry in embargo_data.get('embargoed_countries', []):
        if embargo_entry.get('country') == importing_country:
            return embargo_entry.get('restrictions', None)
    return None
