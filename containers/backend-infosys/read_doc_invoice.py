from prompt_resp_using_llm import get_answer, is_goods_perishable
import json
from read_doc_using_di import extract_doc

# Define the template
prompt = f"""You are a helpful assistant. Please extract 
            - Destination
            field from the given context in a json format.
            Use only the given content to extract the requested information.
            Please provide NA if requested attribute is not present in the given context.
            Please provide the name of the attributes in same case as mentioned in this prompt.
            Please provide only the JSON content and no other content especially '''json'''"""


def remove_text_from_notice(input_text):
    # Find the position of "Notice Concerning Carriers" and truncate the text from there
    keyword = "Payment Due Date "
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
        json_object1 = json.loads(jsonString) 
        return json_object1
    except:
        print(jsonString)
        return None

def get_invoice_data(path_to_document):

     return extract_content_json(path_to_document)  

if __name__ == "__main__":

    file_path = r"C:\Users\bhanumurthi_t\OneDrive - Infosys Limited\Desktop\IATA POC\IATA PoC data\ANA\Sample2-1_205-11111111(LIVE PLANT).pdf"

    print(get_invoice_data(file_path))
