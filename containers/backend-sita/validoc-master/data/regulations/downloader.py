import requests

def update_json_with_downloads(json_data):
    """
    Fetch data from URLs in the JSON and update the JSON with the downloaded content.
    """
    for section, content in json_data.get("cargo_requirements", {}).items():
        if isinstance(content, list):  # Iterate over lists in the JSON
            for item in content:
                if isinstance(item, dict):  # Check if the list contains dictionaries
                    for key, value in item.items():
                        if key == "source" and isinstance(value, str) and value.startswith("http"):
                            try:
                                # Download the data from the URL
                                response = requests.get(value)
                                response.raise_for_status()
                                downloaded_data = response.text
                                
                                # Add the downloaded content under a new key
                                item["downloaded_content"] = downloaded_data
                            except requests.exceptions.RequestException as e:
                                print(f"Failed to download from {value}: {e}")

    return json_data

# Example usage
with open("input.json", "r") as file:
    json_data = json.load(file)

updated_json_data = update_json_with_downloads(json_data)

# Save the updated JSON to a new file
with open("updated_output.json", "w") as file:
    json.dump(updated_json_data, file, indent=4)
