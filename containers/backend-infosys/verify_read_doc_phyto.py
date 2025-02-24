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
            Please provide only the JSON content and no other content especially ```json'''.
            Please provide the name of attributes in the exact same case as mentioned in this prompt 
            irrespective of how it is present in the content, especially for Place of Origin"""


def extract_content_json(path_to_sample_documents):

    doc_1=extract_doc(path_to_sample_documents)
    text = doc_1['content']
    
    answerObject = get_answer(input_query=prompt, context_messages=[text])

    json_object = json.loads(answerObject)

    return parse_json_response(json_object["choices"][0]["message"]["content"])



def parse_json_response(jsonString) :
    try:
        print(jsonString)
        json_object1 = json.loads(jsonString) 
        return json_object1
    except:
        print(jsonString)
        return None

def get_phyto_data(path_to_document):

    jsonObj = extract_content_json(path_to_document)

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
        print(f"{fieldName} -- {value} -- {not value}")
        if value:
            return value
        else:
            raise Exception(f"Error while reading the content for the attribute - {fieldName}")
    except Exception as e:
        raise Exception(f"Error while reading the content for the attribute - {fieldName}")    

if __name__ == "__main__":

    file_path = r"C:\Users\bhanumurthi_t\OneDrive - Infosys Limited\Desktop\IATA POC\IATA PoC data\Qatar\Sample AWBs & Phytocertificate\PyotoCerti_Sample_2.pdf"
    print(f"Response : {get_phyto_data(file_path)}")