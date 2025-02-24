from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import DocumentAnalysisFeature, AnalyzeResult
from prompt_resp_using_llm import get_answer, is_goods_perishable
import re,json,configparser

def extract_doc( path_to_sample_documents, isNatureOfGoodsRequired ):

    config = configparser.ConfigParser()
    config.read('config.ini')

    endpoint = config['DEFAULT']['di.endpoint']
    key = config['DEFAULT']['di.key']

    document_intelligence_client = DocumentIntelligenceClient (
                                        endpoint=endpoint, 
                                        credential=AzureKeyCredential(key)
                                    )
    
    with open(path_to_sample_documents, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
                    "prebuilt-layout",
                    analyze_request=f,
                    features=[DocumentAnalysisFeature.KEY_VALUE_PAIRS],
                    content_type="application/octet-stream",
                )

    result: AnalyzeResult = poller.result()

    extracted_data = {}  # Dictionary to store the key-value pairs
    
    if result.key_value_pairs:
        for kv_pair in result.key_value_pairs:
            if kv_pair.key and kv_pair.value:  # Ensure both key and value exist
                key_content = kv_pair.key.content.strip()
                value_content = kv_pair.value.content.strip()
                extracted_data[key_content] = value_content  

    #To read Nature of the goods, as it is not properly read and kept inside key value pair.
    if isNatureOfGoodsRequired :

        natureOfGoods = ""
        columnIndex = 0
        
        if result.tables:
            for table in result.tables:
                for cell in table.cells:
                    #print(f"{cell.content} --- {cell.row_index} ---- {cell.column_index}")                
                    if re.search("Nature and Quantity of Goods", cell.content):
                        columnIndex = cell.column_index
                    if columnIndex != 0 and columnIndex == cell.column_index and cell.row_index == 2:
                        natureOfGoods = cell.content

        extracted_data["NatureOfGoods"] = natureOfGoods                    
    
    return extracted_data

def get_awb_data(path_to_document):

    extracted_data = extract_doc(path_to_document, True)

    awbObj = {}

    try:
        awbObj = {
            'origin': extract_field_from_object(extracted_data,'Airport of Departure (Addr. of first Carrier) and requested Routing'), 
            'destination' : extract_field_from_object(extracted_data,'Airport Of Destination'),
            'transit' : '',
            'date' : extract_field_from_object(extracted_data,'Executed on (date)'),
            'goodbeingtransported' : extract_field_from_object(extracted_data,'NatureOfGoods'),
            'weight' : extract_field_from_object(extracted_data,'Gross Weight'), 
        }
    except Exception as e:
        awbObj = None    

    return awbObj

def extract_field_from_object(extracted_data, fieldName):
    try:
        return extracted_data[fieldName]
    except Exception as e:
        print(f"Error while reading the content for the attribute - {fieldName}")
        raise Exception(f"Error while reading the content for the attribute - {fieldName}")
   

if __name__ == '__main__':
    path_to_sample_documents_phyto = r"C:\Users\bhanumurthi_t\OneDrive - Infosys Limited\Desktop\IATA POC\IATA PoC data\LATAM\SCL-MAD Flower\Phytosanitary Certificate.pdf"

    path_to_sample_documents_awb = r"C:\Users\bhanumurthi_t\OneDrive - Infosys Limited\Desktop\IATA POC\AWB2.pdf"

    awb_content = extract_doc(path_to_sample_documents_awb, False)
    print(awb_content)
    #phyto_content = extract_doc(path_to_sample_documents_phyto, False)

    #prompt = """From the provided Air WayBill content and Phytosanitory content, please let me know 
     #       a Yes or No answer whether the airport of departure of the goods are matching from the both the contents."""
    #context_messages = ["Air WayBill Content :"+json.dumps(awb_content, indent=4), 
     #                   "Phytosanitory certificate Content :"+json.dumps(phyto_content, indent=4)]
    #answerObject = get_answer(input_query=prompt, context_messages=context_messages)

    #print(answerObject)