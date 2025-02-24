def validate_document_details(document_details):
    """Validate required keys in document details and return missing keys."""
    required_keys = {'awb_number': 'AWB Number', 'shipper': {'name': 'Shipper Name', 'address': 'Shipper Address'}, 'consignee': {'name': 'Consignee Name', 'address': 'Consignee Address'}, 'issuing_carrier_agent': {'name': 'Issuing Carrier Agent Name'}, 'cargo': {'pieces': 'Number of Pieces', 'weight': 'Weight', 'unit': 'Weight Unit', 'description': 'Cargo Description'}, 'additional_details': {'charge': 'Freight Charges', 'charge_currency': 'Currency'}}
    missing_required = []
    missing_optional = []

    def check_keys(key, value):
        if isinstance(value, dict):
            for subkey, subvalue in value.items():
                check_keys(f'{key}.{subkey}', subvalue)
        elif not value or 'error' in str(value).lower() or 'null' in str(value).lower():
            missing_optional.append(key)
    for key, value in document_details.items():
        check_keys(key, value)
    return (missing_required, missing_optional)
