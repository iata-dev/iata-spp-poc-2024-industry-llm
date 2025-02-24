from validaton_backend import *
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(override=True)

validation_path = 'C:\\Users\\schernykh\\OneDrive - Microsoft\\Documents\\work\\clients\\IATA\\PoC data\\validation cases\\Test Cases'

validation_folders = [entry for entry in os.listdir(validation_path) if os.path.isdir(os.path.join(validation_path, entry))]

validation_run = {}

for folder in validation_folders:
   
    # Only validate the QRTC4 folder
    # if folder not in ['QRTC4']:
        # continue

    validation_folder_case = os.listdir(validation_path +"\\"+ folder)

    submitted_documents_dict = {}
    input_image_list = []
    analyzed_files = []

    for file in validation_folder_case:
        if file.lower().endswith('.pdf'):
            pdf_path = validation_path + "\\" + os.path.join(folder, file)
            with open(pdf_path, 'rb') as f:
                data = f.read()
                analyzed_files.append(data)
                image_list = pdf_to_base64_jpeg([data], file)
                input_image_list.extend(image_list)
        

        # On the last iteration, set the `submitted_documents_dict` to be used in the validation process
        if file == validation_folder_case[-1]:
            submitted_documents_dict = {'input_image_list':input_image_list}

    response_dict = visual_prompt_validate_documents(submitted_documents_dict)
    
    # Convert response_dict to JSON and write to disk
    # response_dict["validation_rules"] and corresponding `response` JSON contain the validation results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    json_path = os.path.join(validation_path, folder, f'response_{timestamp}.json')
    with open(json_path, 'w') as json_file:
        json.dump(response_dict, json_file, indent=4)

    validation_run[folder] = response_dict

print(validation_run)
print("validation run complete!")