import os

def get_all_json_files():
    """Get all JSON files from the output folder."""
    if not os.path.exists(output_folder):
        return []
    return [os.path.join(output_folder, f) for f in os.listdir(output_folder) if f.endswith('.json')]

