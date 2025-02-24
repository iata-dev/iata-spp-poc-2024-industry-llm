from prompt_resp_using_llm import get_answer
import json
import base64

import io, os
from flask import Flask, request, jsonify
from read_doc_awb import extract_doc


def get_countries_json(context) :

    input_prompt = """Please extract 
            - Country Of Origin 
            - Country Of Destination
            fields from the given context. 
            Provide me the country of the Airport of Departure and Airport of Destination 
            in small letters without a space in a json format which can be parsed.
            For few countries usa, uae, nz provide abbreviated names and for the remaining 
            provide full names. For all the countries in european union, provide it as eu.
            Attribute names should be origin and destination.
            Please provide only the JSON content and no other content especially ```json  and '''"""
    
    context_messages = [f"Context: {context } "]

    answer = get_answer(input_query=input_prompt, context_messages=context_messages)

    json_object = json.loads(answer)

    return json_object["choices"][0]["message"]["content"]

def get_required_docs_using_llm(origin_required_docs, dest_required_docs, data) :

    input_prompt = f"""Given context consists of document requirements for Origin and Destination
                    airports. Please provide me the list of documents for the {data['nature_of_goods']}
                     goods for both Origin and Destination airports. 
                    Provide only the documents required for {data['nature_of_goods']} goods, 
                    no other documents to be included. The context also provides the list of all the 
                    mandatory documents at the destination, please inclde the same in the response along
                    with any other documents derived.
                    Please provide the content in a JSON format as a list of documents for source 
                    and destination and include the source and destination airport's country as well.
                    Please provide only the JSON content and no other content especially ```json  and '''"""
    
    context_messages = [f"Origin Required Docs: {origin_required_docs } "]
    context_messages.append(f"Destination Required Docs: {dest_required_docs } ")
    context_messages.append(f"Mandatory Destination Docs: {data['list_of_mandatory_documents'] } ")

    answer = get_answer(input_query=input_prompt, context_messages=context_messages)

    json_object = json.loads(answer)

    return json_object["choices"][0]["message"]["content"]

def remove_text_from_notice(input_text):
    # Find the position of "Notice Concerning Carriers" and truncate the text from there
    keyword = "ORIGINAL "
    position = input_text.find(keyword)
    if position != -1:
        return input_text[:position].strip()
    return input_text  # Return the original text if the keyword is not found

def get_required_docs(data) :

    countries_json =  get_countries_json(data)

    print(f" Countries JSON : {countries_json}")

    json_object = json.loads(countries_json)

    origin_file_content = read_file_content(f"docs_required/origin_{json_object["origin"]}.txt")

    dest_file_content = read_file_content(f"docs_required/dest_{json_object["destination"]}.txt")

    docs_required = get_required_docs_using_llm(origin_file_content, dest_file_content, data)

    return docs_required

def read_file_content(file_path):
    if not os.path.exists(file_path):
        print(f"File for the given country doesn't exist. {file_path}")
        return ""
    with open(file_path, 'rb') as f:
        return f.read()
    

# Allow only certain types of files to be uploaded (optional)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def api_required_docs(request):

    data = request.json
    errors = validate_inputs(data)

    if errors:
        return jsonify({"errors": errors}), 400  # Bad Request
    
    # Check if 'list_of_mandatory_documents' attribute exists, if not, add it
    if 'list_of_mandatory_documents' not in data:
        data['list_of_mandatory_documents'] = []
    
    # Process the saved file as needed
    # For example, call your get_awb_data function
    try:
        # Code that may raise an exception

        if data['return_additional_documents'] :
            result = get_required_docs(data)
        else :
            result = {
                        "origin": {
                            "country": data['country_of_origin'],
                            "documents": data['list_of_mandatory_documents']
                        },
                        "destination": {
                            "country": data['country_of_destination'],
                            "documents": data['list_of_mandatory_documents']
                        }
}
    except Exception as e:
        print(f"Exception occurred while processing the required documents : {e}")
        return jsonify({'error': 'Invalid AWB Input'}), 500

    return result, 200

def validate_inputs(data):
    
    errors = []

    # Validate Country of Origin
    if not isinstance(data.get('country_of_origin'), str) or not data['country_of_origin']:
        errors.append("Country of Origin must be a non-empty string.")

    # Validate Country of Destination
    if not isinstance(data.get('country_of_destination'), str) or not data['country_of_destination']:
        errors.append("Country of Destination must be a non-empty string.")

    # Validate Nature of Goods
    if not isinstance(data.get('nature_of_goods'), str) or not data['nature_of_goods']:
        errors.append("Nature of Goods must be a non-empty string.")

    # Validate returnAdditionalDocuments
    if not isinstance(data.get('return_additional_documents'), bool):
        errors.append("returnAdditionalDocuments must be a boolean.")

    return errors

    

if __name__ == "__main__":

    file_path = r"C:\Users\bhanumurthi_t\OneDrive - Infosys Limited\Desktop\IATA POC\IATA PoC data\LATAM\SCL-MAD Flower\AWB.pdf"

    print(get_required_docs(file_path))
    

