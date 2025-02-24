from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import DocumentAnalysisFeature, AnalyzeResult
from prompt_resp_using_llm import get_answer

def extract_doc(key, endpoint, path_to_sample_documents):
    document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    with open(path_to_sample_documents, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-layout",
            analyze_request=f,
            features=[DocumentAnalysisFeature.KEY_VALUE_PAIRS],
            content_type="application/octet-stream",
        )
    result: AnalyzeResult = poller.result()
    return result

endpoint = "https://resource-di-605792.cognitiveservices.azure.com/"
key = "Bp61La9q0i62Vd3vP8znCOI5pwFVlD2nl42Qx0df6jO9cC3QZGFlJQQJ99ALACYeBjFXJ3w3AAALACOGjnqb"

path_to_sample_documents = r"C:\Users\bhanumurthi_t\OneDrive - Infosys Limited\Desktop\IATA POC\AWB2.pdf"

doc_1=extract_doc(key, endpoint, path_to_sample_documents)

text = doc_1['content']

def remove_text_from_notice(input_text):
    # Find the position of "Notice Concerning Carriers" and truncate the text from there
    keyword = "ORIGINAL "
    position = input_text.find(keyword)
    if position != -1:
        return input_text[:position].strip()
    return input_text  # Return the original text if the keyword is not found

cleaned_text = remove_text_from_notice(text)
print(cleaned_text)



# Define the template
template = """
You are a helpful assistant. You are given a shipment document, and your task is to extract and structure the relevant information in JSON format.
Document Content: {content}

- Shipper's Name and Address 
- Consignee's Name and Address
- Air Waybill
- Issuing Carrier's Agent Name and City
- Issued by
- Freight
- Nature and Quantity of Goods
- Airport of Destination
- Airport of Departure and requested Routing
- Declared Value for Carriage
- Declared Value for Customs
- Handling Informations
- No. of Pieces RCP
- Gross weight
- chargeable weight 
"""

print(template)



from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import (
    ChatPromptTemplate
    #FewShotChatMessagePromptTemplate,
)
from operator import itemgetter

from typing import Optional, Any
import requests
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM


class CustomLLM(LLM):
     
    endpoint: str
    #api_key: str

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, run_manager: Optional[CallbackManagerForLLMRun] = None, **kwargs: Any) -> str:
        payload = {
            "prompt": prompt,
            "max_tokens": 1500
        }

        headers = {
            'Content-Type': 'application/json'
            #'api_key': self.api_key
        }

        response = requests.post(self.endpoint, headers=headers, json=payload)
        
        if response.ok:
            data = response.json()
            generated_text= data.get('response')  # Extracting text directly
            return generated_text  # Extracting text directly
        else:
            response.raise_for_status()
#'http://veaiscoem-01:5000/igpt/ai_wrapper/models/gpt/v4o-mini'
# Creating a new object 
new_llm_2 = CustomLLM(endpoint='http://veaiscoem-01:5000/igpt/ai_wrapper/models/gpt/v35')
                      #api_key='e5801c8221c74bda9258c09950fac338'

llm=new_llm_2

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


# Define the PromptTemplate with your template string
prompt = PromptTemplate(input_variables=["content"], template=template)

# Create the chain that will use the LLM and the prompt template
chain = LLMChain(prompt=prompt, llm=llm)

# Generate the result using the chain
result = chain.run(content=cleaned_text)

# Print the generated JSON
print(f"abc - {result}")