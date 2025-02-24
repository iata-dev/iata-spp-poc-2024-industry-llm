from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import DocumentAnalysisFeature, AnalyzeResult
import io

import re,json,configparser

config = configparser.ConfigParser()
config.read('config.ini')

endpoint = config['DEFAULT']['di.endpoint']
key = config['DEFAULT']['di.key']

def extract_doc(path_to_sample_documents):

    document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, 
                                                              credential=AzureKeyCredential(key))
    with open(path_to_sample_documents, "rb") as f:

        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-layout",
            analyze_request=f,
            features=[DocumentAnalysisFeature.KEY_VALUE_PAIRS],
            content_type="application/octet-stream",
        )

    print("Got poller object")    
    result: AnalyzeResult = poller.result()
    print("Got Result object") 
    return result

def extract_doc_using_content(file_content):

    content_stream = io.BytesIO(file_content)

    document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, 
                                                              credential=AzureKeyCredential(key))
    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-layout",
        analyze_request=content_stream,
        features=[DocumentAnalysisFeature.KEY_VALUE_PAIRS],
        content_type="application/octet-stream",
    )

    result: AnalyzeResult = poller.result()

    text = result['content']    

    return text

def get_content_using_di(file_path):
    doc_1 = extract_doc(file_path)
    text = doc_1['content']    
    return text


