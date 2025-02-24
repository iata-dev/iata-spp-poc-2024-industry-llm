from prompt_resp_using_llm import get_answer, is_goods_perishable
import json
from read_doc_using_di import extract_doc
import re

# Define the template
prompt = f"""You are a helpful assistant. Please extract 
            - Airport of Departure 
            - Airport of Destination
            - Nature and Quantity of Goods
            - Gross Weight
            - Executed on ( only date, not place)
            fields from the given context in a json format which can be parsed.
            Please provide only the JSON content and no other content especially ```json  and '''"""


def remove_text_from_notice(input_text):
    # Find the position of "Notice Concerning Carriers" and truncate the text from there
    keyword = "ORIGINAL "
    position = input_text.find(keyword)
    if position != -1:
        return input_text[:position].strip()
    return input_text  # Return the original text if the keyword is not found


def extract_content_json(path_to_sample_documents):

    doc_1=extract_doc(path_to_sample_documents)
    text = doc_1['content']
    cleaned_text = remove_text_from_notice(text)    
    
    answerObject = get_answer(input_query=prompt, context_messages=[cleaned_text])

    json_object = json.loads(answerObject)


    return parse_json_response(json_object["choices"][0]["message"]["content"])

def parse_json_response(jsonString) :
    try:
        print(f"Object Returned from LLM : {jsonString}")
        json_object1 = json.loads(jsonString)
        return json_object1
    except:
        print(jsonString)
        return None

def get_awb_data(path_to_document):

    jsonObj = extract_content_json(path_to_document)

    if jsonObj :
        awbObj = {}

        try:
            awbObj = {
                'origin': get_field(jsonObj,'Airport of Departure'), 
                'destination' : get_field(jsonObj,'Airport of Destination'),
                'transit' : '',
                'date' : get_field(jsonObj,'Executed on'),
                'goodbeingtransported' : get_field(jsonObj,'Nature and Quantity of Goods'),
                'weight' : get_field(jsonObj,'Gross Weight'), 
                'classofgoods' : get_class_of_goods(
                                    is_goods_perishable(
                                        get_field(jsonObj,'Nature and Quantity of Goods')
                                    )
                                )
            }

        except Exception as e:
            print(f"An error occurred: {e}")
            awbObj = None 
    else:   
        awbObj = None 

    return awbObj

def get_field(jsonObj, fieldName):

    try:
        value = jsonObj[fieldName].strip()
        print(f"{fieldName} -- {value} -- {not value}")
        if value:
            return value
        else:
            raise Exception(f"Error while reading the content for the attribute - {fieldName}")
    except Exception as e:
        raise Exception(f"Error while reading the content for the attribute - {fieldName}")    

def get_class_of_goods(areGoodsPerishable) :
    if "Yes" in areGoodsPerishable:
        return "Perishable"
    else:
        return "Non-Perishable"

if __name__ == "__main__":

    file_path = r"C:\Users\bhanumurthi_t\OneDrive - Infosys Limited\Desktop\IATA POC\IATA PoC data\LATAM\SCL-MIA-MAD Flower transit\AWB.pdf"
    
    print(f" AWB Object : {get_awb_data(file_path)}")