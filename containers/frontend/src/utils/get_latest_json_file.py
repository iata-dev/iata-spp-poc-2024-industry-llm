import os

def get_latest_json_file():
    """Get the latest JSON file from the output folder."""
    if not os.path.exists(output_folder):
        return None
    json_files = [os.path.join(output_folder, f) for f in os.listdir(output_folder) if f.endswith('.json')]
    if not json_files:
        return None
    latest_file = max(json_files, key=os.path.getmtime)
    return latest_file

