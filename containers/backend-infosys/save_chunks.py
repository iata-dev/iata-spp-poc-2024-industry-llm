import json
import os

def are_chunks_available(file_path):
    return  os.path.exists(file_path) and os.path.getsize(file_path) > 0   

def save_chunks(chunks, file_path) :
    with open(file_path, 'w') as json_file:
        json.dump(chunks, json_file, indent=4)

def load_chunks(file_path) :
    chunks = []
    with open(file_path, 'r') as json_file:
        chunks = json.load(json_file)

    return chunks

if __name__ == "__main__":
    chunks = {
        "name": "Bhanumurthi 1234",
        "age": 39,
        "city": "Tampa",
        "email": "bhanumurthi_t@infosys.com"
    }

    file_path = 'data/data.json'

    save_chunks(chunks=chunks, file_path=file_path)
    print(f"Data has been successfully saved to {file_path}.")