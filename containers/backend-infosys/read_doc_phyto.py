from prompt_resp_using_llm import get_answer, is_goods_perishable
import json
from read_doc_using_di import extract_doc

# Define the template
prompt = f"""You are a helpful assistant. Please extract 
            - Place of Origin
            - Declared point of entry
            - name of produce
            - declared quantity 
            - Date
            fields from the given context in a json format. 
            Please provide name of produce and declared quantity as separate fields.
            The value for these fields is separated by comma.
            If name of produce contains multiple values combine it as a single comma separated string.
            Also for the quantity, if contains more than one, please provide only one value with sum of 
            all the values and provide it as string type. If the quantity is not properly specified 
            with the correct units (e.g., kg, grams), please indicate the value as NA.
            Quantity mentioned in like stems or equivelant word in other languares 
            ( eg. tallos in spanish ) etc should be consideren invalid quantity.
            Please provide the name of the attributes in same case as mentioned in this prompt.
            Please provide only the JSON content and no other content especially '''json'''"""


def extract_content_json(path_to_sample_documents):

    doc_1=extract_doc(path_to_sample_documents)
    text = doc_1['content']
    
    answerObject = get_answer(input_query=prompt, context_messages=[text])

    json_object = json.loads(answerObject)

    return parse_json_response(json_object["choices"][0]["message"]["content"])



def parse_json_response(jsonString) :
    try:
        json_object1 = json.loads(jsonString) 
        return json_object1
    except:
        print(jsonString)
        return None

def get_phyto_data(path_to_document):

    jsonObj = extract_content_json(path_to_document)

    print(f"Phyto Object : {jsonObj}")

    awbObj = {}

    if jsonObj :

        try:
            awbObj = {
                'origin': get_field(jsonObj,'Place of Origin'), 
                'destination' : get_field(jsonObj,'Declared point of entry'),
                'date' : get_field(jsonObj,'Date'),
                'goodbeingtransported' : get_field(jsonObj,'name of produce'),
                'weight' : get_field(jsonObj,'declared quantity'),             
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
        if value:
            return value
        else:
            raise Exception(f"Error while reading the content for the attribute - {fieldName}")
    except Exception as e:
        raise Exception(f"Error while reading the content for the attribute - {fieldName}")    

if __name__ == "__main__":

    file_path = r"C:\Users\bhanumurthi_t\OneDrive - Infosys Limited\Desktop\IATA POC\IATA PoC data\LATAM\SCL-MAD Flower\Phytosanitary Certificate.pdf"

    print(get_phyto_data(file_path))