import json

def calculate_total_cargo_weight():
    """Calculate the total cargo weight from all JSON files."""
    total_weight = 0
    json_files = get_all_json_files()
    for json_file in json_files:
        try:
            with open(json_file, 'r') as file:
                data = json.load(file)
                weight = float(data.get('document_details', {}).get('cargo', {}).get('weight', 0))
                total_weight += weight
                print(total_weight)
        except Exception as e:
            print(f'Error processing file {json_file}: {e}')
    return total_weight

