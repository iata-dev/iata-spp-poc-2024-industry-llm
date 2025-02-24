import json
import os

def load_json_data():
    """Load JSON data from the latest file."""
    latest_file = get_latest_json_file()
    if latest_file and os.path.exists(latest_file):
        with open(latest_file, 'r') as file:
            return json.load(file)
    return {}

