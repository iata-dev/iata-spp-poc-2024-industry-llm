from prompt_resp_using_llm import get_answer, is_goods_perishable
import json
from read_doc_using_di import extract_doc

# Define the template
prompt = f"""You are a helpful assistant. Please extract 
            - Airport of Departure 
            - Airport of Destination
            - Nature and Quantity of Goods
            - No. of Pieces
            - Gross Weight
            - Total
            - Chargeable Weight
            - Rate
            - Executed on ( only date, not place)
            - Shipper Name
            - Shipper Address
            - Consignee Name
            - Consignee Address
            - Issuing Carrier Agent Name
            - Issuing Carrier City
            - Agent IATA Code
            - Shipper Country Code
            - Consignee Country Code
            - Document Prefix
            - Document Number
            - Handling Information
            fields from the given context in a json format.
            Use only the given content to extract the requested information.
            Please provide NA if requested attribute is not present in the given context.
            Please provide the name of the attributes in same case as mentioned in this prompt.
            Derive the country code of shipper and consignee based on the Shipper's name and address
            and Consignee's Name and address fields respectively.
            Please consider to fetch Gross Weight filed the one which is
            represented after the No. of pieces field. Also for Gross weight, please don't
            cosider to fetch from AV.GROSS WEIGHT field instead consider only Gross Weight field.
            Please provide only the JSON content and no other content especially '''json'''"""


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
        json_object1 = json.loads(jsonString) 
        return json_object1
    except:
        print(jsonString)
        return None

def get_awb_data(path_to_document,require_class_of_goods):

    jsonObj = extract_content_json(path_to_document)

    print(f" AWB JSON Object : {jsonObj}")

    if jsonObj :
        awbObj = {}

        try:
            awbObj = {
                'origin': get_field(jsonObj,'Airport of Departure'), 
                'destination' : get_field(jsonObj,'Airport of Destination'),
                'transit' : '',
                'Executed On Date' : get_field(jsonObj,'Executed on'),
                'goodbeingtransported' : get_field(jsonObj,'Nature and Quantity of Goods'),
                'weight' : get_field(jsonObj,'Gross Weight'), 
                
                'Shipper Name' : get_field(jsonObj,'Shipper Name'),
                'Shipper Address' : get_field(jsonObj,'Shipper Address'),
                'Consignee Name' : get_field(jsonObj,'Consignee Name'),
                'Consignee Address' : get_field(jsonObj,'Consignee Address'),
                'Agent Name' : get_field(jsonObj,'Issuing Carrier Agent Name'),
                'Agent City' : get_field(jsonObj,'Issuing Carrier City'),
                'Agent IATA Code' : get_field(jsonObj,'Agent IATA Code'),
                'Number Of Pieces' : get_field(jsonObj,'No. of Pieces'),
                'Shipper Country Code' : get_field(jsonObj,'Shipper Country Code'),
                'Consignee Country Code' : get_field(jsonObj,'Consignee Country Code'),
                'Document Prefix' : get_field(jsonObj,'Document Prefix'),
                'Document Number' : get_field(jsonObj,'Document Number'),
                'Handling Information' : get_field(jsonObj,'Handling Information')                
            }

            if(require_class_of_goods) :
                awbObj['classofgoods'] = get_class_of_goods(
                                        is_goods_perishable(
                                            get_field(jsonObj,'Nature and Quantity of Goods')
                                        )
                                    )

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

def get_class_of_goods(areGoodsPerishable) :
    if "Yes" in areGoodsPerishable:
        return "Perishable"
    else:
        return "Non-Perishable"

if __name__ == "__main__":

    file_path = r"C:\Users\bhanumurthi_t\OneDrive - Infosys Limited\Desktop\IATA POC\IATA PoC data\LATAM\SCL-MAD Flower\Basic-Outlines.pdf"

    print(get_awb_data(file_path))
