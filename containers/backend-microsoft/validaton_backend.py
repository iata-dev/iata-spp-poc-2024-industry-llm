from openai import AzureOpenAI
import instructor
# import os
from typing import List, Literal
from pdf2image import convert_from_bytes
from io import BytesIO
import base64
from pydantic import BaseModel, Field
import time
import os
from dotenv import load_dotenv
# import json

# set the environment variables needed to call the GPT4o model deployed to Azure OpenAI
load_dotenv(override=True)


def ocr_analyze_read(doc_bytes):
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.ai.documentintelligence.models import DocumentAnalysisFeature, AnalyzeResult, AnalyzeDocumentRequest

    # # For how to obtain the endpoint and key, please see PREREQUISITES above.
    endpoint = os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"]
    key = os.environ["DOCUMENTINTELLIGENCE_API_KEY"]

    document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-read",
        AnalyzeDocumentRequest(bytes_source=doc_bytes),
        features=[DocumentAnalysisFeature.LANGUAGES]
    )       
    result: AnalyzeResult = poller.result()
    return result


def pdf_to_base64_jpeg(file_byte_list: list, file_name: str):
    base64_images = []

    for document_path in file_byte_list:
        images = convert_from_bytes(document_path, fmt='jpeg', poppler_path =".\\poppler\\" )
        # file_name = os.path.basename(document_path)
        # Convert PDF pages to images
        for index, image in enumerate(images):
            # Save image to a BytesIO object in JPEG format
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            # Encode the image to base64
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            base64_images.append(
                    {
                    "document_entity_name":f"page {index+1} of \'{file_name}\'"
                    ,"image_base64":img_str
                    }
                )
    

    return base64_images

def LLM_visual_call(response_model: object, input_image: str, input_prompt: str):

    # instantiate the client
    client = instructor.from_openai(AzureOpenAI())

    # call the model
    model_response = client.chat.completions.create(
        model="gpt-4o",
        response_model=response_model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"{input_prompt}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{input_image}"}}
                ]
            }
        ],
    )

    return model_response

def LLM_text_call(response_model: object, user_input_info: str, input_prompt: str):

    # instantiate the client
    client = instructor.from_openai(AzureOpenAI())

    # call the model
    model_response = client.chat.completions.create(
        model="gpt-4o",
        response_model=response_model,
        messages=[
            {
                "role": "system",
                "content": input_prompt
            },
            {
                "role": "user",
                "content": user_input_info
            }
        ],
    )

    return model_response

def aggregate_validation_to_markdown(input_dict_document_master: dict):
    markdown_string_validation_success = ""
    markdown_string_validation_failed = ""

    all_validation_passed = True
    # for every document in the list
    for index, value in enumerate(input_dict_document_master['validation_rules']['fundamental_rules']):

        validation_result_check = input_dict_document_master['validation_rules']['fundamental_rules'][index]['rule_validation_status']
        if validation_result_check == 'PASSED':
            markdown_string_validation_success += f":violet[**{input_dict_document_master['validation_rules']['fundamental_rules'][index]['rule_description']}**]  "
            markdown_string_validation_success += f" *(Rule origin: {input_dict_document_master['validation_rules']['fundamental_rules'][index]['rule_origin']})* \n\n"
            markdown_string_validation_success += f"**:green[Rule {validation_result_check}]**: {input_dict_document_master['validation_rules']['fundamental_rules'][index]['rule_validation_result_comment']} \n\n --- \n\n"

        # we only want to show the rules that were explicitly failed
        elif validation_result_check == 'FAILED':
            markdown_string_validation_failed += f":violet[**{input_dict_document_master['validation_rules']['fundamental_rules'][index]['rule_description']}**]  "
            markdown_string_validation_failed += f" *(Rule origin: {input_dict_document_master['validation_rules']['fundamental_rules'][index]['rule_origin']})* \n\n"
            markdown_string_validation_failed += f"**:red[Rule {validation_result_check}]**: {input_dict_document_master['validation_rules']['fundamental_rules'][index]['rule_validation_result_comment']} \n\n --- \n\n"
            all_validation_passed = False
    # for every document in the list
    for index, value in enumerate(input_dict_document_master['validation_rules']['situation_specific_rules']):

        validation_result_check = input_dict_document_master['validation_rules']['situation_specific_rules'][index]['rule_validation_status']
        if validation_result_check == 'PASSED':
            markdown_string_validation_success += f":violet[**{input_dict_document_master['validation_rules']['situation_specific_rules'][index]['rule_description']}**]  "
            markdown_string_validation_success += f" *(Rule origin: {input_dict_document_master['validation_rules']['situation_specific_rules'][index]['rule_origin']})* \n\n"
            markdown_string_validation_success += f"**:green[Rule {validation_result_check}]**: {input_dict_document_master['validation_rules']['situation_specific_rules'][index]['rule_validation_result_comment']} \n\n --- \n\n"
        # we only want to show the rules that were explicitly failed
        elif validation_result_check == 'FAILED':
            markdown_string_validation_failed += f":violet[**{input_dict_document_master['validation_rules']['situation_specific_rules'][index]['rule_description']}**] "
            markdown_string_validation_failed += f" *(Rule origin: {input_dict_document_master['validation_rules']['situation_specific_rules'][index]['rule_origin']})* \n\n"
            markdown_string_validation_failed += f"**:red[Rule {validation_result_check}]**: {input_dict_document_master['validation_rules']['situation_specific_rules'][index]['rule_validation_result_comment']} \n\n --- \n\n"
            all_validation_passed = False

    # for every document in the list
    for index, value in enumerate(input_dict_document_master['validation_rules']['carrier_rules']):
        validation_result_check = input_dict_document_master['validation_rules']['carrier_rules'][index]['rule_validation_status']
        if validation_result_check == 'PASSED':
            markdown_string_validation_success += f":violet[**{input_dict_document_master['validation_rules']['carrier_rules'][index]['rule_description']}**]  "
            markdown_string_validation_success += f" *(Rule origin: {input_dict_document_master['validation_rules']['carrier_rules'][index]['rule_origin']})* \n\n"
            markdown_string_validation_success += f"**:green[Rule {validation_result_check}]**: {input_dict_document_master['validation_rules']['carrier_rules'][index]['rule_validation_result_comment']} \n\n --- \n\n"
        # we only want to show the rules that were explicitly failed
        elif validation_result_check == 'FAILED':
            markdown_string_validation_failed += f":violet[**{input_dict_document_master['validation_rules']['carrier_rules'][index]['rule_description']}**] "
            markdown_string_validation_failed += f" *(Rule origin: {input_dict_document_master['validation_rules']['carrier_rules'][index]['rule_origin']})* \n\n"
            markdown_string_validation_failed += f"**:red[Rule {validation_result_check}]**: {input_dict_document_master['validation_rules']['carrier_rules'][index]['rule_validation_result_comment']} \n\n --- \n\n"
            all_validation_passed = False
    
    # combine all the markdown strings
    # if the `all_validation_passed` is True, then only the success string will be returned
    # final_markdown_string = ("# VALIDATION SUCCESFUL! \n" + markdown_string_validation_success) if all_validation_passed == True else ("# VALIDATION FAILED! \n" + markdown_string_validation_failed + markdown_string_validation_success)
    final_markdown_string = (markdown_string_validation_success) if all_validation_passed == True else (markdown_string_validation_failed + markdown_string_validation_success)
    return final_markdown_string, all_validation_passed
                                                                        


def aggregate_documents_to_markdown(input_dict_document_master: dict):
    # create a markdown string
    markdown_string_awb = ""
    markdown_string_phytosanitary = ""
    markdown_string_dangerous_goods = ""
    markdown_string_cites_certificate = ""
    markdown_string_neppex_certificate = ""
    markdown_invoice = ""
    markdown_string_packing_list = ""

    # for every document in the list
    for index, value in enumerate(input_dict_document_master['input_image_list']):
        # get the document type label
        document_type = input_dict_document_master['input_image_list'][index]['LLM_visual_document_type']

        if document_type == 'AIRWAY BILL':
            markdown_string_awb += f"# Document Type:\n {document_type} \n"
            
            markdown_string_awb += f"## Document name and page: \n {input_dict_document_master['input_image_list'][index]['document_entity_name']}\n"
            
            markdown_string_awb += "## Document details: \n"
            
            # markdown_string_awb += f"### DRY ICE USAGE:\n {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['dry_ice_usage_label'][0]}\n"
            
            markdown_string_awb += f"### AIRWAY BILL ID:\n\n {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['airway_bill_id']}\n"
            
            markdown_string_awb += f"### DATE:\n\n {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['date_execution']}\n"
            
            markdown_string_awb += f"### COUNTRY OF ORIGIN:\n\n the cargo is being shipped FROM: {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['country_of_origin_label']}\n"
            
            markdown_string_awb += f"### COUNTRY OF DESTINATION:\n\n the cargo is being shipped TO: {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['country_of_destination_label']}\n"
            
            markdown_string_awb += f"### CARGO HANDLING INFORMATION:\n\n the customer has requested the following handling instructions: {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['cargo_handling_information_extract']}\n"
            
            markdown_string_awb += f"### NATURE OF CARGO:\n\n the general information on the cargo: {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['nature_of_cargo_extact']}\n"
            
            markdown_string_awb += f"### CARGO GROSS WEIGHT:\n\n  {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['cargo_gross_weight']}\n"
            
            markdown_string_awb += f"### CARGO ITEMS DETAILS: \n"
            
            for item in input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['cargo_items_list']:
                markdown_string_awb += f"#### ITEM DESCRIPTION: \n{item['item_description']}\n"
                markdown_string_awb += f"#### PERISHIBLE CARGO TYPE: \n{item['perishible_cargo_type'][0]}\n"
                # markdown_string_awb += f"#### TEMPERATURE CONTROL REQUESTED: \n{item['temperature_control_requested'][0]}\n"
                markdown_string_awb += f"#### ITEM WEIGHT: \n {item['item_weight']} {item['item_weight_metric'][0]}\n"
                markdown_string_awb += f"#### ITEM NUMBER OF RCP PIECES: \n {item['item_number_rcp_pieces']}\n"
        
        elif document_type == 'PHYTOSANITARY CERTIFICATE':
            #extract the int part of the weight string using regex
            import re
            weight_str = input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['cargo_gross_weight']
            weight_match = re.search(r'\d+', weight_str)
            gross_cargo_weight = float(weight_match.group()) if weight_match else 0.0

            markdown_string_phytosanitary += f"# Document Type:\n {document_type} \n"
            
            markdown_string_phytosanitary += f"## Document name and page: \n {input_dict_document_master['input_image_list'][index]['document_entity_name']}\n"
            
            markdown_string_phytosanitary += "## Document details: \n"
            
            markdown_string_phytosanitary += f"### ORGANIZATION CERTIFIED BY:\n {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['organization_certified_by']}\n"

            markdown_string_phytosanitary += f"### DATE:\n\n {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['date_execution']}\n"
            
            markdown_string_phytosanitary += f"### COUNTRY OF ORIGIN:\n the cargo is being shipped FROM: {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['country_of_origin_label']}\n"
            
            markdown_string_phytosanitary += f"### COUNTRY OF DESTINATION:\n the cargo is being shipped TO: {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['country_of_destination_label']}\n"
            
            markdown_string_phytosanitary += f"### CARGO GROSS WEIGHT:\n\n {gross_cargo_weight} (acceptable 5% air waybill range = min:{gross_cargo_weight*0.95}  max:{gross_cargo_weight*1.05}) \n"
           
            markdown_string_phytosanitary += f"### CARGO ITEMS DETAILS: \n"
            
            for item in input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['cargo_items_list']:
                markdown_string_phytosanitary += f"#### ITEM DESCRIPTION: \n{item['item_description']}\n"
                markdown_string_phytosanitary += f"#### PERISHIBLE CARGO TYPE: \n{item['perishible_cargo_type'][0]}\n"
                # markdown_string_phytosanitary += f"#### TEMPERATURE CONTROL REQUESTED: \n{item['temperature_control_requested'][0]}\n"
                markdown_string_phytosanitary += f"#### ITEM WEIGHT: \n {item['item_weight']} {item['item_weight_metric'][0]}\n"
                markdown_string_phytosanitary += f"#### ITEM NUMBER OF RCP PIECES: \n {item['item_number_rcp_pieces']}\n"
        
        # elif document_type == 'DANGEROUS GOODS CERTIFICATE':
        #     markdown_string_dangerous_goods += f"# Document Type:\n {document_type} \n"
            
        #     markdown_string_dangerous_goods += f"## Document name and page: \n {input_dict_document_master['input_image_list'][index]['document_entity_name']}\n"
            
        #     markdown_string_dangerous_goods += "## Document details: \n"
            
        #     markdown_string_dangerous_goods += f"### COUNTRY OF ORIGIN:\n the cargo is being shipped by air FROM: {input_dict_document_master
        #     ['input_image_list'][index]['LLM_visual_extracted_details']['country_of_origin_label']}\n"
            
        #     markdown_string_dangerous_goods += f"### COUNTRY OF DESTINATION:\n the cargo is being shipped by air TO: {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['country_of_destination_label']}\n"
            
        #     markdown_string_dangerous_goods += f"### CARGO ITEMS DETAILS: \n"
            
        #     for item in input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['cargo_items_list']:
        #         markdown_string_dangerous_goods += f"#### ITEM DESCRIPTION: \n  {item['item_description']}\n"
        #         markdown_string_dangerous_goods += f"#### PERISHIBLE CARGO TYPE: \n {item['perishible_cargo_type'][0]}\n"
        #         markdown_string_dangerous_goods += f"#### TEMPERATURE CONTROL REQUESTED: \n     {item['temperature_control_requested'][0]}\n"

        elif document_type == 'CITES CERTIFICATE':
            markdown_string_cites_certificate += f"# Document Type:\n {document_type} \n"
            
            markdown_string_cites_certificate += f"## Document name and page: \n {input_dict_document_master['input_image_list'][index]['document_entity_name']}\n"
            
            markdown_string_cites_certificate += "## Document details: \n"
            
            markdown_string_cites_certificate += f"### DATE:\n\n {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['date_execution']}\n"

            markdown_string_cites_certificate += f"### COUNTRY OF ORIGIN:\n the cargo is being shipped by air FROM: {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['country_of_origin_label']}"
            
            markdown_string_cites_certificate += f"\n### COUNTRY OF DESTINATION:\n the cargo is being shipped by air TO: {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['country_of_destination_label']}\n"
            
            markdown_string_cites_certificate += f"### CARGO GROSS WEIGHT:\n\n  {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['cargo_gross_weight']}\n"
            
            markdown_string_cites_certificate += f"### CARGO ITEMS DETAILS: \n"
            
            for item in input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['cargo_items_list']:
                markdown_string_cites_certificate += f"#### ITEM DESCRIPTION: \n  {item['item_description']}\n"
                markdown_string_cites_certificate += f"#### PERISHIBLE CARGO TYPE: \n {item['perishible_cargo_type'][0]}\n"
                markdown_string_cites_certificate += f"#### ITEM WEIGHT: \n {item['item_weight']} {item['item_weight_metric'][0]}\n"
                markdown_string_cites_certificate += f"#### ITEM NUMBER OF RCP PIECES: \n {item['item_number_rcp_pieces']}\n"

        elif document_type == 'NEPPEX':
            markdown_string_neppex_certificate += f"# Document Type:\n {document_type} \n"
            
            markdown_string_neppex_certificate += f"## Document name and page: \n {input_dict_document_master['input_image_list'][index]['document_entity_name']}\n"
            
            markdown_string_neppex_certificate += "## Document details: \n"

            markdown_string_neppex_certificate += f"### DATE:\n\n {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['date_execution']}\n"
            
            markdown_string_neppex_certificate += f"\n### COUNTRY OF ORIGIN:\n the cargo is being shipped by air FROM: {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['country_of_origin_label']}"
            
            markdown_string_neppex_certificate += f"### COUNTRY OF DESTINATION:\n the cargo is being shipped by air TO: {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['country_of_destination_label']}\n"
            
            markdown_string_neppex_certificate += f"### CARGO GROSS WEIGHT:\n\n  {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['cargo_gross_weight']}\n"
            
            markdown_string_neppex_certificate += f"### CARGO ITEMS DETAILS: \n"
            
            for item in input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['cargo_items_list']:
                markdown_string_neppex_certificate += f"#### ITEM DESCRIPTION: \n  {item['item_description']}\n"
                markdown_string_neppex_certificate += f"#### PERISHIBLE CARGO TYPE: \n {item['perishible_cargo_type'][0]}\n"
                markdown_string_neppex_certificate += f"#### ITEM WEIGHT: \n {item['item_weight']} {item['item_weight_metric'][0]}\n"
                markdown_string_neppex_certificate += f"#### ITEM NUMBER OF RCP PIECES: \n {item['item_number_rcp_pieces']}\n"
    
        elif document_type == 'INVOICE':
            markdown_invoice += f"# Document Type:\n {document_type} \n"
            
            markdown_invoice += f"## Document name and page: \n {input_dict_document_master['input_image_list'][index]['document_entity_name']}\n"
            
            markdown_invoice += "## Document details: \n"
            
            markdown_invoice += f"### DATE:\n\n {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['date_execution']}\n"

            markdown_invoice += f"\n### COUNTRY OF ORIGIN:\n the cargo is being shipped by air FROM: {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['country_of_origin_label']}"
            
            markdown_invoice += f"### COUNTRY OF DESTINATION:\n the cargo is being shipped by air TO: {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['country_of_destination_label']}\n"
            
            markdown_invoice += f"### CARGO GROSS WEIGHT:\n\n  {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['cargo_gross_weight']}\n"

            markdown_invoice += f"### CARGO ITEMS DETAILS: \n"
            
            for item in input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['cargo_items_list']:
                markdown_invoice += f"#### ITEM DESCRIPTION: \n  {item['item_description']}\n"
                markdown_invoice += f"#### PERISHIBLE CARGO TYPE: \n {item['perishible_cargo_type'][0]}\n"
                markdown_invoice += f"#### ITEM WEIGHT: \n {item['item_weight']} {item['item_weight_metric'][0]}\n"
                markdown_invoice += f"#### ITEM NUMBER OF RCP PIECES: \n {item['item_number_rcp_pieces']}\n"
    
        elif document_type == 'PACKING LIST':
            markdown_string_packing_list += f"# Document Type:\n {document_type} \n"
            
            markdown_string_packing_list += f"## Document name and page: \n {input_dict_document_master['input_image_list'][index]['document_entity_name']}\n"
            
            markdown_string_packing_list += "## Document details: \n"
            
            markdown_string_packing_list += f"### DATE:\n\n {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['date_execution']}\n"
            
            markdown_string_packing_list += f"\n### COUNTRY OF ORIGIN:\n the cargo is being shipped by air FROM: {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['country_of_origin_label']}"
            
            markdown_string_packing_list += f"### COUNTRY OF DESTINATION:\n the cargo is being shipped by air TO: {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['country_of_destination_label']}\n"
            
            markdown_string_packing_list += f"### CARGO GROSS WEIGHT:\n\n  {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['cargo_gross_weight']}\n"

            markdown_string_packing_list += f"### CARGO ITEMS DETAILS: \n"
            
            for item in input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['cargo_items_list']:
                markdown_string_packing_list += f"#### ITEM DESCRIPTION: \n  {item['item_description']}\n"
                markdown_string_packing_list += f"#### PERISHIBLE CARGO TYPE: \n {item['perishible_cargo_type'][0]}\n"
                markdown_string_packing_list += f"#### ITEM WEIGHT: \n {item['item_weight']} {item['item_weight_metric'][0]}\n"
                markdown_string_packing_list += f"#### ITEM NUMBER OF RCP PIECES: \n {item['item_number_rcp_pieces']}\n"
    
    # combine all the markdown strings
    final_markdown_string = markdown_string_awb + markdown_string_phytosanitary + markdown_string_dangerous_goods + markdown_string_cites_certificate + markdown_string_packing_list + markdown_invoice + markdown_string_neppex_certificate
    return final_markdown_string


def get_instructor_class(class_name_arg : str):
    class Document_classifier(BaseModel):
        """Analysis of a single page of a set of documents incluced with `Airway Export document set`, submitted by user for validation. Each document contains important info on the cargo being shipped by air. Classify the document type using the image provided"""
    
        document_type_label: Literal["AIRWAY BILL", "AIR FREIGHT MANIFEST","PHYTOSANITARY CERTIFICATE","DANGEROUS GOODS CERTIFICATE", "CITES CERTIFICATE", "CARGO MANIFEST", "INVOICE", "HEALTH CERTIFICATE","PACKING LIST","CERTIFICATE OF ORIGIN","NEPPEX","OTHER"] = Field(
            ...,
            description="Predicted 'type of documenent' label for the document analyzed as part `Airway Export document set`, submitted by user for validation. Only a certain types of document are allowed. If the document is for `Convention on International Trade in Endangered Species of Wild Fauna and Flora`, return CITES. If the document has any mention of `NEPPEX`or `Notificación de Embarque de Productos Pesqueros para Exportación`, then return `NEPPEX`. If the document is not one of the specific types, return OTHER label.",
        )
        document_type_explanation: str = Field(
            ...,
            description="The chain of thought that led to the predicted 'type of documenent' label.",
        )
 
        document_language: List[Literal["ENGLISH", "FRENCH", "SPANISH", "GERMAN", "JAPANESE","OTHER"]] = Field(
            ...,
            description="The language mainly used in the document. If the document is not in one of the specified languages, return OTHER label.",
        )
    
    class Cargo_item(BaseModel):
        item_description: str = Field (
            ...,
            description="Description of the items being shipped. This could include the item name, quantity, weight, and other relevant information.",
        )
        item_weight: str = Field (
            ...,
            description="The weight of the items being shipped. Usually in Kilograms (Kg). Prefer `GROSS WEIGHT` over `AV. GROSS WEIGHT`. Return an empty string if no mention.",
        )
        item_weight_metric: List[Literal["KG", "LB", "TON", "OTHER"]] = Field(
            ...,
            description="The metric used to measure the weight of the items being shipped. Usually `K`=KG and `L`=LB. return OTHER if there is no appropriate match.",
        )
        item_number_rcp_pieces: str = Field (
            ...,
            description="The number of pieces RCP (Rate Combination Point) for the items being shipped. Return an empty string if no mention.",
        )
        perishible_cargo_type: List[Literal["FRESH PRODUCE","LIVE ANIMALS","FLOWERS","OTHER PLANTS","SEAFOOD","SHELLFISH","PHARMACEUTICAL","FROZEN FOOD", "OTHER FOOD","OTHER"]] = Field(
            ...,
            description="Type of cargo being shipped. If the cargo is not perishable, return OTHER label.",
        )
        # temperature_control_requested: List[Literal["YES", "NO"]] = Field(
        #     ...,
        #     description="Whether the airwaybill mentions a request for temperature control during transportation for this specific cargo item. If no temperature control is mentioned, return NO label.",
        # )

    class Phytosanitary_certificate(BaseModel):
        organization_certified_by: str = Field(
            ...,
            description="Name of the organization that has certified the document as a Phytosanitary Certificate. Return the name of the organization in ENGLISH, if the language is not ENGLISH.",
        )
        
        country_of_origin_label: str = Field(
            ...,
            description="Predicted 'country of origin' label for the document analyzed. The origin country is where the air cargo is being shipped FROM.  Use the full name of the country, such as France or Spain, for United States of America put `USA`. If there is no such information, return an empty string. Return an ENGLISH translation, if the language is not ENGLISH.",
        )

        country_of_origin_explanation: str = Field(
            ...,
            description="The chain of thought that led to the predicted 'country_of_origin' label.",
        )
        
        country_of_destination_label: str = Field(
            ...,
            description="Predicted 'country of destination' label for the document analyzed. The destination country is where the air cargo is being shipped TO. Use the full name of the country, such as France or Spain, for United States of America put `USA`. If there is no such information, return an empty string. Return an ENGLISH translation, if the language is not ENGLISH.",
        )
        
        country_of_destination_explanation: str = Field(
            ...,
            description="The chain of thought that led to the predicted 'country_of_destination' label.",
        )

        cargo_items_list: List[Cargo_item] = Field(
            ...,
            description="List of cargo items mentioned on the document being shipped by air. Each item contains a description, perishable cargo type, and temperature control request.",
        )

        fumigation_performed_label: List[Literal["YES", "NO"]] = Field(
            ...,
            description="Predicted 'fumigation performed' label for the document analyzed. Fumigation is a common requirement for international cargo shipments. If no mention is made, return NO label.",
        )
        date_execution: str = Field(
            ...,
            description="Predicted 'date of execution' in the format DD-MM-YYYY on which the document was executed or submitted. If there is no such information, return an empty string.",
        )
        
        date_execution_explanation: str = Field(
            ...,
            description="The chain of thought that led to the predicted of the 'date_execution' field .",
        )

        cargo_gross_weight: str = Field(
            ...,
            description="Extracted gross weight of the cargo, as described in the document. If there is no such information, return an empty string.",
        )
        
        cargo_gross_weight_explanation: str = Field(
            ...,
            description="The chain of thought that led to the 'cargo_gross_weight' extraction.",
        )

    # class Dangerous_goods_certificate(BaseModel):
        
    #     country_of_origin_label: str = Field(
    #         ...,
    #         description="Predicted 'country of origin' label for the document analyzed. The origin country is where the air cargo is being shipped FROM. Use the full name of the country, such as France or Spain, for United States of America put `USA`. If there is no such information, return an empty string. Return an ENGLISH translation, if the language is not ENGLISH.",
    #     )

    #     country_of_origin_explanation: str = Field(
    #         ...,
    #         description="The chain of thought that led to the predicted 'country_of_origin' label.",
    #     )
        
    #     country_of_destination_label: str = Field(
    #         ...,
    #         description="Predicted 'country of destination' label for the document analyzed. The destination country is where the air cargo is being shipped TO. Use the full name of the country, such as France or Spain, for United States of America put `USA`. If there is no such information, return an empty string. Return an ENGLISH translation, if the language is not ENGLISH.",
    #     )
        
    #     country_of_destination_explanation: str = Field(
    #         ...,
    #         description="The chain of thought that led to the predicted 'country_of_destination' label.",
    #     )

    #     cargo_items_list: List[Cargo_item] = Field(
    #         ...,
    #         description="List of cargo items mentioned on the document being shipped by air. Each item contains a description, perishable cargo type, and temperature control request.",
    #     )

    class CITES_certificate(BaseModel):
        
        country_of_origin_label: str = Field(
            ...,
            description="Predicted 'country of origin' label for the document analyzed. The origin country is where the air cargo is being shipped FROM. Use the full name of the country, such as France or Spain, for United States of America put `USA`. If there is no such information, return an empty string. Return an ENGLISH translation, if the language is not ENGLISH.",
        )

        country_of_origin_explanation: str = Field(
            ...,
            description="The chain of thought that led to the predicted 'country_of_origin' label.",
        )
        
        country_of_destination_label: str = Field(
            ...,
            description="Predicted 'country of destination' label for the document analyzed. The destination country is where the air cargo is being shipped TO. Use the full name of the country, such as France or Spain, for United States of America put `USA`. If there is no such information, return an empty string. Return an ENGLISH translation, if the language is not ENGLISH.",
        )
        
        country_of_destination_explanation: str = Field(
            ...,
            description="The chain of thought that led to the predicted 'country_of_destination' label.",
        )

        cargo_items_list: List[Cargo_item] = Field(
            ...,
            description="List of cargo items mentioned on the document being shipped by air. Each item contains a description, perishable cargo type and other relevant information.",
        )
        cargo_gross_weight: str = Field(
            ...,
            description="Extracted gross weight of the cargo, as described in the document. If there is no such information, return an empty string.",
        )
        
        cargo_gross_weight_explanation: str = Field(
            ...,
            description="The chain of thought that led to the 'cargo_gross_weight' extraction.",
        )

    class NEPPEX_certificate(BaseModel):
        
        country_of_origin_label: str = Field(
            ...,
            description="Predicted 'country of origin' label for the document analyzed. The origin country is where the air cargo is being shipped FROM. Use the full name of the country, such as France or Spain, for United States of America put `USA`. If there is no such information, return an empty string. Return an ENGLISH translation, if the language is not ENGLISH.",
        )

        country_of_origin_explanation: str = Field(
            ...,
            description="The chain of thought that led to the predicted 'country_of_origin' label.",
        )
        
        country_of_destination_label: str = Field(
            ...,
            description="Predicted 'country of destination' label for the document analyzed. The destination country is where the air cargo is being shipped TO. Use the full name of the country, such as France or Spain, for United States of America put `USA`. If there is no such information, return an empty string. Return an ENGLISH translation, if the language is not ENGLISH.",
        )
        
        country_of_destination_explanation: str = Field(
            ...,
            description="The chain of thought that led to the predicted 'country_of_destination' label.",
        )

        cargo_items_list: List[Cargo_item] = Field(
            ...,
            description="List of cargo items mentioned on the document being shipped by air. Each item contains a description and other relevant information.",
        )
        date_execution: str = Field(
            ...,
            description="Predicted 'date of execution' in the format DD-MM-YYYY on which the document was executed or submitted. If there is no such information, return an empty string.",
        )
        
        date_execution_explanation: str = Field(
            ...,
            description="The chain of thought that led to the predicted of the 'date_execution' field .",
        )
        cargo_gross_weight: str = Field(
            ...,
            description="Extracted gross weight of the cargo, as described in the document. If there is no such information, return an empty string.",
        )
        
        cargo_gross_weight_explanation: str = Field(
            ...,
            description="The chain of thought that led to the 'cargo_gross_weight' extraction.",
        )

    class Packing_list(BaseModel):
        
        country_of_origin_label: str = Field(
            ...,
            description="Predicted 'country of origin' label for the document analyzed. The origin country is where the air cargo is being shipped FROM. Use the full name of the country, such as France or Spain, for United States of America put `USA`. If there is no such information, return an empty string. Return an ENGLISH translation, if the language is not ENGLISH.",
        )

        country_of_origin_explanation: str = Field(
            ...,
            description="The chain of thought that led to the predicted 'country_of_origin' label.",
        )
        
        country_of_destination_label: str = Field(
            ...,
            description="Predicted 'country of destination' label for the document analyzed. The destination country is where the air cargo is being shipped TO. Use the full name of the country, such as France or Spain, for United States of America put `USA`. If there is no such information, return an empty string. Return an ENGLISH translation, if the language is not ENGLISH.",
        )
        
        country_of_destination_explanation: str = Field(
            ...,
            description="The chain of thought that led to the predicted 'country_of_destination' label.",
        )

        cargo_items_list: List[Cargo_item] = Field(
            ...,
            description="List of cargo items mentioned on the document being shipped by air. Each item contains a description and other relevant information.",
        )
        
        date_execution: str = Field(
            ...,
            description="Predicted 'date of execution' in the format DD-MM-YYYY on which the document was executed or submitted. If there is no such information, return an empty string.",
        )
        
        date_execution_explanation: str = Field(
            ...,
            description="The chain of thought that led to the predicted of the 'date_execution' field .",
        )
        cargo_gross_weight: str = Field(
            ...,
            description="Extracted gross weight of the cargo, as described in the document. If there is no such information, return an empty string.",
        )
        
        cargo_gross_weight_explanation: str = Field(
            ...,
            description="The chain of thought that led to the 'cargo_gross_weight' extraction.",
        )

    class Invoice(BaseModel):
        
        country_of_origin_label: str = Field(
            ...,
            description="Predicted 'country of origin' label for the document analyzed. The origin country is where the air cargo is being shipped FROM. Use the full name of the country, such as France or Spain, for United States of America put `USA`. If there is no such information, return an empty string. Return an ENGLISH translation, if the language is not ENGLISH.",
        )

        country_of_origin_explanation: str = Field(
            ...,
            description="The chain of thought that led to the predicted 'country_of_origin' label.",
        )
        
        country_of_destination_label: str = Field(
            ...,
            description="Predicted 'country of destination' label for the document analyzed. The destination country is where the air cargo is being shipped TO. Use the full name of the country, such as France or Spain, for United States of America put `USA`. If there is no such information, return an empty string. Return an ENGLISH translation, if the language is not ENGLISH.",
        )
        
        country_of_destination_explanation: str = Field(
            ...,
            description="The chain of thought that led to the predicted 'country_of_destination' label.",
        )

        cargo_items_list: List[Cargo_item] = Field(
            ...,
            description="List of cargo items mentioned on the document being shipped by air. Each item contains a description and other relevant information.",
        )

        date_execution: str = Field(
            ...,
            description="Predicted 'date of execution' in the format DD-MM-YYYY on which the document was executed or submitted. If there is no such information, return an empty string.",
        )
        
        date_execution_explanation: str = Field(
            ...,
            description="The chain of thought that led to the predicted of the 'date_execution' field .",
        )
        cargo_gross_weight: str = Field(
            ...,
            description="Extracted gross weight of the cargo, as described in the document. If there is no such information, return an empty string.",
        )
        
        cargo_gross_weight_explanation: str = Field(
            ...,
            description="The chain of thought that led to the 'cargo_gross_weight' extraction.",
        )
        


    class Airway_bill(BaseModel):
        """Analysis of a single page of a document that is part of the `Airway Bill document set`, submitted by user for validation. Each document contains important info on the cargo being shipped by air. Extract required information which will be used to validate against IATA and local regulations"""

        airway_bill_id: str = Field(
            ...,
            description="Extracted ID of Airway Bill type of document. If there is no such information, return an empty string.",
        )

        airway_bill_id_explanation: str = Field(
            ...,
            description="The chain of thought that led to the 'airway_bill_id' extraction.",
        )

        air_carrier_label: List[Literal["LATAM", "ALL NIPPON AIRWAYS", "QATAR AIRWAYS", "OTHER"]] = Field(
            ...,
            description="Extracted name of the issuing air carrier that will be transporting the cargo (usually founs under `Issued by`). If there is no such information, return `OTHER`",
        )

        air_carrier_explanation: str = Field(
            ...,
            description="The chain of thought that led to the 'air_carrier_label' extraction.",
        )
        
        shipper_name_label: str = Field(
            ...,
            description="Extracted name of the shipper that is sending the cargo. Sometimes `shipper` is also referred to as `exporter` or `consigner`. If there is no such information, return an empty string.",
        )

        shipper_name_explanation: str = Field(
            ...,
            description="The chain of thought that led to the 'shipper_name_label' extraction.",
        )

        shipper_address_label: str = Field(
            ...,
            description="Extracted address of the shipper that is sending the cargo. Sometimes `shipper` is also referred to as `exporter` or `consigner`. If there is no such information, return an empty string.",
        )

        shipper_address_explanation: str = Field(
            ...,
            description="The chain of thought that led to the 'shipper_address_label' extraction.",
        )

        consignee_name_label: str = Field(
            ...,
            description="Extracted name of the consignee that is sending the cargo. Sometimes `consignee` is also referred to as `receiver` or `consigner`. If there is no such information, return an empty string.",
        )

        consignee_name_explanation: str = Field(
            ...,
            description="The chain of thought that led to the 'shipper_name_label' extraction.",
        )

        consignee_address_label: str = Field(
            ...,
            description="Extracted address of the shipper that is sending the cargo. Sometimes `shipper` is also referred to as `exporter` or `consigner`. If there is no such information, return an empty string.",
        )

        consignee_address_explanation: str = Field(
            ...,
            description="The chain of thought that led to the 'shipper_address_label' extraction.",
        )

        # dry_ice_usage_label: List[Literal["NO", "USED"]] = Field(
        #     ...,
        #     description="Perishable cargo sometimes needs temperature control via dry ice usage. Dry Ice can be also mentioned as `Carbon dioxide, solid` If no mention is made, return NO label.",
        # )
        
        # dry_ice_usage_explanation: str = Field(
        #     ...,
        #     description="The chain of thought that led to the predicted 'dry ice usage' label.",
        # )

        # handling_temperature_band_check: List[Literal["NO", "SINGLE", "MULTIPLE"]] = Field(
        #     ...,
        #     description="Check if the handling instructions include specifications on the temperature bands that are needed for the cargo. If a single band is mentioned, return 'SINGLE'; if multiple temperature bands are mentioned, return 'MULIPLE'; if no mention is made, return NO label.",
        # )
        
        # handling_temperature_band_check_explanation: str = Field(
        #     ...,
        #     description="The chain of thought that led to the predicted 'handling_temperature_band_check' label.",
        # )

        country_of_origin_label: str = Field(
            ...,
            description="Predicted 'country of origin' label for the document analyzed, submitted by user for validation. Use the 'Airport of Origin' field, if available. Use the full name of the country, such as France or Spain, for United States of America put `USA`. The origin country is where the air cargo is being shipped FROM. Between `airport of origin` and `shipper's country` -- ALWAYS PRIORITIZE the `airport of origin`. If there is no such information, return an empty string.",
        )
        
        country_of_origin_explanation: str = Field(
            ...,
            description="The chain of thought that led to the predicted 'country_of_origin' label.",
        )
        
        # origin_airport_code_label: str = Field(
        #     ...,
        #     description="Predicted 'origin airport code' 3 letter IATA label for the document analyzed as part `Airway Export document set`, submitted by user for validation. The origin airport is where the air cargo is being shipped FROM. If there is no such information, return an empty string.",
        # )

        country_of_destination_label: str = Field(
            ...,
            description="Predicted 'country of destination' label for the document analyzed, submitted by user for validation. Use the 'Airport of Destination' field, if available. Use the full name of the country, such as France or Spain, for United States of America put `USA`. The destination country is where the air cargo is being shipped TO. If there is no such information, return an empty string.",
        )
        
        country_of_destination_explanation: str = Field(
            ...,
            description="The chain of thought that led to the predicted 'country_of_destination' label.",
        )
        
        # destination_airport_code_label: str = Field(
        #     ...,
        #     description="Predicted 'destination airport code' 3 letter IATA label for the document analyzed as part `Airway Export document set`, submitted by user for validation. The destination airport is where the air cargo is being shipped TO. If there is no such information, return an empty string.",
        # )

        country_of_transit_label: str = Field(
            ...,
            description="Predicted 'country of transit' label for the document analyzed. Use the full name of the country, such as France or Spain, for United States of America put `USA`. The transit country is where the air cargo will visit for a brief time before going to the country of destination. If there is no such information, return an empty string.",
        )
        
        country_of_transit_explanation: str = Field(
            ...,
            description="The chain of thought that led to the predicted 'country_of_transit' label.",
        )
        
        # transit_airport_code_label: str = Field(
        #     ...,
        #     description="Predicted 'transit airport code' label for the document analyzed as part `Airway Export document set`, submitted by user for validation. The transit airport is where the air cargo will visit for a brief time before going to the country of destination. If there is no such information, return an empty string.",
        # )

        cargo_handling_information_extract: str = Field(
            ...,
            description="Extracted 'cargo handling information' exactly is it appears on the document. These might include instructions on the storage temperature and other conditions important when transporting perishable cargo by air travel. If there is no handling information, return an empty string.",
        )
        
        cargo_handling_information_explanation: str = Field(
            ...,
            description="The chain of thought that led to the 'handling_information' extraction.",
        )

        nature_of_cargo_extact: str = Field(
            ...,
            description="Extracted description of the nature of the transported cargo, including details on  type, status, condition, dimensions, size and quantity of the cargo. For the Airway Bill type of document, use the field `nature and quantity of goods`. Extracted information will be used to help assess applicable regulation for air transport ation under IATA and local jurisdictions. If there is no such information, return an empty string.",
        )
        
        nature_of_cargo_explanation: str = Field(
            ...,
            description="The chain of thought that led to the 'nature_of_cargo' extraction.",
        )

        cargo_items_list: List[Cargo_item] = Field(
            ...,
            description="List of cargo items mentioned on the airway bill being shipped by air. Each item contains a description, perishable cargo type and other relevant information.",
        )
        
        date_execution: str = Field(
            ...,
            description="Predicted 'date of execution' in the format DD-MM-YYYY on which the airway bill was executed or submitted. If there is no such information, return an empty string.",
        )
        
        date_execution_explanation: str = Field(
            ...,
            description="The chain of thought that led to the predicted of the 'date_execution' field .",
        )

        cargo_gross_weight: str = Field(
            ...,
            description="Extracted gross weight of the cargo, as described in the document. If there is no such information, return an empty string.",
        )
        
        cargo_gross_weight_explanation: str = Field(
            ...,
            description="The chain of thought that led to the 'cargo_gross_weight' extraction.",
        )
        
        # cargo_total_charge_extract: str = Field(
        #     ...,
        #     description="Extracted total charge incurred by the air transportation of the cargo, as described in the document. If there is no such information, return an empty string.",
        # )
        
        # cargo_total_charge_extract_explanation: str = Field(
        #     ...,
        #     description="The chain of thought that led to the 'cargo_total_charge' extraction.",
        # )

    class validation_issues_identified(BaseModel):
        """The detailed description of the issues that were identified during the validation of information of a document against the Airway Bill information"""
        
        validation_issue_description: str = Field(
            ...,
            description="Detailed description of the validation issue identified during the validation process",
        )

    class validate_phytosanitary_certificate(BaseModel):
        """Validation of the markdown which contains information extracted from the phytosanitary certificate and the Airway Bill. The phytosanitary certificate is required for the export of plants, flowers, and fresh produce."""
    
        validation_status: List[Literal["PASSED", "FAILED"]] = Field(
            ...,
            description="The overall validation status of the phytosanitary certificate information against the Airway Bill. If the information matches, return PASSED; otherwise, return FAILED. #VALIDATION RULES \n\n 1. The information should match the country of origin, country of destination, and the general cargo items details. \n\n 2. Validate gross weight versus Air Waybill bill, the acceptable range of divergeance is +/- 5% \n\n 3. When validating items details, it is acceptable to have some discrepencies that are technical in nature, as the airway bill tends to have a high-level view descriptions of the items. \n\n 4. The class of the items should match overall (such as `Dendrobium flowers` = `Orchids`). \n\n 5. The date of the certificate should be equal or smaller than the date on the air waybill \n\n 6. Only SEAFOOD, SHELLFISH, FLOWERS, OTHER PLANTS, FRESH PRODUCE, and OTHER FOOD require a phytosanitary certificate so if a certain cargo item present on an Airway Bill is missing from the phytosanitary certificate, it should not be necessarly considered as a validation issue. \n\n 7. Use your best judgement and justify in the 'validation_status_explanation' field.",
        )
        
        validation_status_explanation: str = Field(
            ...,
            description="The chain of thought that led to 'validation_status'",
        )
 
        validation_issues: List[validation_issues_identified] = Field(
            ...,
            description="The detailed description of the issues that were identified during the validation of information of a document against the Airway Bill information",
        )

    class validate_phytosanitary_certificate_qatar(BaseModel):
        """Validation of the markdown which contains information extracted from the phytosanitary certificate and the Airway Bill, as per QATAR AIRWAYS requirements. The phytosanitary certificate is required for the export of plants, flowers, and fresh produce."""
    
        validation_status: List[Literal["PASSED", "FAILED"]] = Field(
            ...,
            description="The overall validation status of the phytosanitary certificate information against the Airway Bill. If the information matches, return PASSED; otherwise, return FAILED. #VALIDATION RULES \n\n 1. The information should match the country of origin, country of destination and the cargo items details such as the weight and the number of RCP pieces.  \n\n 2. The class of the items should match overall (such as `Dendrobium flowers` = `Orchids`). \n\n 3. The date of the certificate should be equal or smaller than the date on the air waybill \n\n 4. Use your best judgement and justify in the 'validation_status_explanation' field.",
        )
        
        validation_status_explanation: str = Field(
            ...,
            description="The chain of thought that led to 'validation_status'",
        )
 
        validation_issues: List[validation_issues_identified] = Field(
            ...,
            description="The detailed description of the issues that were identified during the validation of information of a document against the Airway Bill information",
        )

    class validate_packing_list(BaseModel):
        """Validation of the markdown which contains information extracted from the packing list and the Airway Bill. The packing list is required by some air carriers as part of the cargo export document set."""
    
        validation_status: List[Literal["PASSED", "FAILED"]] = Field(
            ...,
            description="The overall validation status of the invoice information against the Airway Bill. If the information matches, return PASSED; otherwise, return FAILED. #VALIDATION RULES \n\n 1. The information should match the *consignee details* , *country of origin*, *country of destination*, and the *cargo items details*. \n\n 2. Don't check the *weight* and the *`RCP number of pieces`*. \n\n 3. Justify your decision in the 'validation_status_explanation' field.",
        )
        
        validation_status_explanation: str = Field(
            ...,
            description="The chain of thought that led to 'validation_status'",
        )
 
        validation_issues: List[validation_issues_identified] = Field(
            ...,
            description="The detailed description of the issues that were identified during the validation of information of a document against the Airway Bill information",
        )

    class validate_invoice(BaseModel):
        """Validation of the markdown which contains information extracted from the invoice document and the Airway Bill. The invoice document is required by some air carriers as part of the cargo export document set."""
    
        validation_status: List[Literal["PASSED", "FAILED"]] = Field(
            ...,
            description="The overall validation status of the invoice information against the Airway Bill. If the information matches, return PASSED; otherwise, return FAILED. #VALIDATION RULES \n\n 1. The information should match the *consignee details* , *country of origin*, *country of destination*, and the *cargo items details*. \n\n 2. Don't check the *weight* and the *`RCP number of pieces`*. \n\n 3. Justify your decision in the 'validation_status_explanation' field.",
        )
        
        validation_status_explanation: str = Field(
            ...,
            description="The chain of thought that led to 'validation_status'",
        )
 
        validation_issues: List[validation_issues_identified] = Field(
            ...,
            description="The detailed description of the issues that were identified during the validation of information of a document against the Airway Bill information",
        )
    

    class validate_CITES_certificate(BaseModel):
        """Validation of the markdown which contains information extracted from the CITES certificate and the Airway Bill."""
    
        validation_status: List[Literal["PASSED", "FAILED"]] = Field(
            ...,
            description="The overall validation status of the CITES certificate information against the Airway Bill. If the information matches, return PASSED; otherwise, return FAILED. The information should match the country of origin, country of destination, and the cargo items. Only the cargo items that have been identified as part of the CITES need to be validated. Use your best judgement and justify in the 'validation_status_explanation' field.",
        )
        
        validation_status_explanation: str = Field(
            ...,
            description="The chain of thought that led to 'validation_status'",
        )
 
        validation_issues: List[validation_issues_identified] = Field(
            ...,
            description="The detailed description of the issues that were identified during the validation of information of a document against the Airway Bill information",
        )

    class validate_NEPPEX_certificate(BaseModel):
        """Validation of the markdown which contains information extracted from the NEPPEX certificate and the Airway Bill."""
    
        validation_status: List[Literal["PASSED", "FAILED"]] = Field(
            ...,
            description="The overall validation status of the NEPPEX certificate information against the Airway Bill. If the information matches, return PASSED; otherwise, return FAILED. Only the cargo items that have been identified as part of the NEPPEX need to be validated. #VALIDATION RULES \n\n 1. The information should match the country of origin, country of destination, and the cargo items.  \n\n 2. Validate gross weight versus Air Waybill bill, the acceptable range of divergeance is +/- 5% \n\n 3. Use your best judgement and justify in the 'validation_status_explanation' field.",
        )
        
        validation_status_explanation: str = Field(
            ...,
            description="The chain of thought that led to 'validation_status'",
        )
 
        validation_issues: List[validation_issues_identified] = Field(
            ...,
            description="The detailed description of the issues that were identified during the validation of information of a document against the Airway Bill information",
        )

    class CITES_items(BaseModel):
        """The detailed description of the items that are part of the CITES list. Extract the items that are part of the CITES list and the chain of thought that led to the 'cites_item_description'"""
        
        cites_item_description: str = Field(
            ...,
            description="Check if the item is part of the following list of CITES items: Balaenoptera edeni,Megaptera novaeangliae , Eretmochelys imbricata , Elephas maximus , Falco hybrid , Falco peregrinus , Falco rusticolus , Acinonyx jubatus , Panthera pardus , Panthera tigris , Balearica pavonina , Gorilla gorilla , Pan troglodytes , Amazona auropalliata , Ara militaris , Primolius maracana , Psittacus erithacus , Diceros bicornis , Gypohierax angolensis , Acipenser gueldenstaedtii , Acipenseridae hybrid , Huso huso , Pachypodium lealii , Balaeniceps rex , Boa constrictor , Candoia aspera , Candoia carinata , Candoia paulsoni , Cacatua alba , Eolophus roseicapilla , Catalaphyllia jardinei , Euphyllia ancora , Euphyllia cristata , Euphyllia glabrescens , Plerogyra sinuosa , Espadarana prosoblepon , Hyalinobatrachium spp. , Hyalinobatrachium colymbiphyllum , Hyalinobatrachium fleischmanni , Sachatamia albomaculata , Cercocebus chrysogaster , Cercopithecus ascanius , Cercopithecus hamlyni , Cercopithecus neglectus , Cercopithecus petaurista , Cercopithecus wolfi , Lophocebus aterrimus , Macaca fascicularis , Miopithecus talapoin , Chamaeleo calyptratus , Furcifer pardalis , Cycas revoluta , Dendrobates auratus , Oophaga vicentei , Duncanopsammia axifuga , Lonchura oryzivora , Euphorbia arida , Euphorbia baliola , Euphorbia braunsii , Euphorbia bupleurifolia , Euphorbia clavarioides , Euphorbia clavigera , Euphorbia decepta , Euphorbia decidua , Euphorbia ecklonii , Euphorbia esculenta , Euphorbia flanaganii , Euphorbia fusca , Euphorbia gatbergensis , Euphorbia horrida , Euphorbia mlanjeana , Euphorbia multiceps , Euphorbia obesa , Euphorbia polygona , Euphorbia rudis , Euphorbia schoenlandii , Euphorbia stellispina , Euphorbia tortirama , Euphorbia tuberosa , Euphorbia umfoloziensis , Euphorbia virosa , Falco cherrug , Caulastraea spp. , Favia danae , Lynx lynx isabellinus , Panthera leo , Fungia spp. , Heliofungia actiniformis , Gekko gecko , Giraffa camelopardalis , Balearica regulorum , Agalychnis callidryas , Iguana iguana , Perodicticus potto , Acanthastrea lordhowensis , Blastomussa spp. , Lobophyllia spp. , Scolymia australis , Symphyllia spp. , Cattleya hybrid , Dendrobium hybrid , Orchidaceae spp. , Orchidaceae hybrid , Phalaenopsis spp. , Spathoglottis hybrid , Vanda hybrid , Echinophyllia spp. , Pavo muticus , Goniopora lobata , Potamotrygon leopoldi , Agapornis fischeri , Amazona aestiva , Amazona albifrons , Amazona amazonica , Amazona autumnalis , Amazona farinosa , Amazona festiva , Amazona ochrocephala , Amazona ventralis , Ara ararauna , Ara chloropterus , Ara severus , Aratinga acuticaudata , Aratinga auricapillus , Aratinga erythrogenys , Aratinga euops , Aratinga finschi , Aratinga jandaya , Aratinga leucophthalma , Aratinga mitrata , Aratinga pertinax , Aratinga solstitialis , Aratinga wagleri , Brotogeris chiriri , Brotogeris chrysoptera , Brotogeris cyanoptera , Brotogeris jugularis , Brotogeris sanctithomae , Brotogeris tirica , Deroptyus accipitrinus , Eclectus roratus , Eupsittula canicularis , Eupsittula nana , Forpus coelestis , Forpus passerinus , Graydidascalus brachyurus , Myiopsitta monachus , Nandayus nenday , Neophema splendida , Neopsephotus bourkii , Pionites leucogaster , Pionites melanocephalus , Pionopsitta pyrilia , Pionus fuscus , Pionus menstruus , Pionus senilis , Pionus sordidus , Pionus tumultuosus , Platycercus elegans , Platycercus eximius , Psittacara holochlorus , Psittacula cyanocephala , Psittacula eupatria , Pyrrhura hoffmanni , Pyrrhura leucotis , Pyrrhura picta , Leiopython albertisii , Malayopython reticulatus , Morelia spilota , Morelia viridis , Python breitensteini , Python brongersmai , Python curtus , Python regius , Pteroglossus aracari , Ramphastos sulfuratus , Ceratotherium simum , Centrochelys sulcata , Chelonoidis carbonarius , Stigmochelys pardalis , Trachyphyllia geoffroyi , Tridacna maxima , Varanus auffenbergi , Varanus doreanus , Varanus dumerilii , Varanus jobiensis , Varanus rudicollis , Varanus salvator , Varanus yuwonoi , Scleractinia spp. , Pelargonium triste",
        )

        cites_item_explanation: str = Field(
            ...,
            description="The chain of thought that led to the 'cites_item_description'",
        )

    class CITES_items_check(BaseModel):
        """Evaluation of whether any of the items on the Airway bill are part of the CITES list. CITES is an international agreement between governments to ensure that international trade in specimens of wild animals and plants does not threaten their survival."""
    
        cites_status_check: List[Literal["NO_CITES", "CITES_DETECTED"]] = Field(
            ...,
            description="The status of the items on the Airway Bill against the CITES list. If no items are part of the CITES list, return NO_CITES; otherwise, return CITES_DETECTED. The items should be checked against the CITES list to determine if they are endangered species. If the items are not part of the CITES list, it should not be considered as a validation issue. Use your best judgement and justify in the 'cites_status_explanation' field.",
        )
        
        cites_status_check_explanation: str = Field(
            ...,
            description="The chain of thought that led to 'cites_status_check'",
        )
 
        cites_item_list: List[CITES_items] = Field(
            ...,
            description="The list of items which were detected to be a part of the CITES list.",
        )
    

    if class_name_arg == "Document_classifier":
        return Document_classifier
    elif class_name_arg == "Airway_bill":
        return Airway_bill
    elif class_name_arg == "Phytosanitary_certificate":
        return Phytosanitary_certificate
    elif class_name_arg == "validate_phytosanitary_certificate":
        return validate_phytosanitary_certificate
    elif class_name_arg == "validate_phytosanitary_certificate_qatar":
        return validate_phytosanitary_certificate_qatar
    elif class_name_arg == "CITES_items_check":
        return CITES_items_check
    elif class_name_arg == "CITES_certificate":
        return CITES_certificate
    elif class_name_arg == "validate_CITES_certificate":
        return validate_CITES_certificate
    elif class_name_arg == "NEPPEX":
        return NEPPEX_certificate
    elif class_name_arg == "validate_NEPPEX_certificate":
        return validate_NEPPEX_certificate
    elif class_name_arg == "Packing_list":
        return Packing_list
    elif class_name_arg == "validate_packing_list":
        return validate_packing_list
    elif class_name_arg == "Invoice":
        return Invoice
    elif class_name_arg == "validate_invoice":
        return validate_invoice

    # elif class_name_arg == "Dangerous_goods_certificate":
    #     return Dangerous_goods_certificate


def visual_prompt_validate_documents(input_dict_document_master: dict, progress_callback=None):
    start_time = time.time()
    input_prompt = "Analyze this document to determine the validity. Use JSON tool to extract the needed information and label the required fields."

    input_dict_document_master['document_types_detected'] = []
    input_dict_document_master['master_awb_carrier'] = ""

    input_dict_document_master['total_tokens_combined'] = 0
    input_dict_document_master['total_tokens_completion'] = 0
    input_dict_document_master['total_tokens_prompt'] = 0
    # for every document in the list
    for index_document_entity, value in enumerate(input_dict_document_master['input_image_list']):
        
        # create a new `LLM_visual_document_type` key in the dictionary for the analyzed document, which will contain the LLM response with the inferred document type
        input_dict_document_master['input_image_list'][index_document_entity]['LLM_visual_document_type'] = {}

        # get the document page image for analysis (in the base64 string format) 
        base64_document_page_for_analysis = input_dict_document_master['input_image_list'][index_document_entity]['image_base64']
        
        #get the OCR read from document intelligence
        doc_ocr_result_obj = ocr_analyze_read(base64_document_page_for_analysis)
        input_dict_document_master['input_image_list'][index_document_entity]['ocr_read'] = doc_ocr_result_obj.content


        # call the LLM model to classify the document type, get back the instructor object
        
        input_prompt = f"Analyze this document using both the image and OCR data of the image provided. Use JSON tool to extract the needed information and label the required fields. \n\n # OCR DATA: \n\n {doc_ocr_result_obj.content}"

        document_classifier_instructor_class = get_instructor_class('Document_classifier')
        LLM_response_instructor_object = LLM_visual_call(document_classifier_instructor_class, base64_document_page_for_analysis, input_prompt)

        # track token usage
        input_dict_document_master['total_tokens_combined'] += LLM_response_instructor_object._raw_response.usage.model_dump()['total_tokens']
        input_dict_document_master['total_tokens_completion'] += LLM_response_instructor_object._raw_response.usage.model_dump()['completion_tokens']
        input_dict_document_master['total_tokens_prompt'] += LLM_response_instructor_object._raw_response.usage.model_dump()['prompt_tokens']

        # convert the instructor object to a dictionary
        LLM_response_dict = LLM_response_instructor_object.model_dump()

        # get the document type label from the converted dictionary
        LLM_inferred_document_type = LLM_response_dict['document_type_label']

        # chain of thought that led to the predicted 'type of documenent' label
        input_dict_document_master['input_image_list'][index_document_entity]['LLM_visual_document_type_COT'] = {}
        input_dict_document_master['input_image_list'][index_document_entity]['LLM_visual_document_type_COT'] = LLM_response_dict['document_type_explanation']

        # language of the document
        input_dict_document_master['input_image_list'][index_document_entity]['LLM_visual_document_language'] = {}  
        input_dict_document_master['input_image_list'][index_document_entity]['LLM_visual_document_language'] = LLM_response_dict['document_language'][0]

        # add the document type label to the dictionary
        input_dict_document_master['input_image_list'][index_document_entity]['LLM_visual_document_type'] = LLM_inferred_document_type

        # Notify progress after setting the inferred document type
        callback_dict_classification = input_dict_document_master['input_image_list'][index_document_entity]
        if progress_callback:
            progress_callback(callback_dict_classification, f"classification")

        # document_type_label: List[Literal["AIRWAY BILL", "AIR FREIGHT MANIFEST","PHYTOSANITARY CERTIFICATE","DANGEROUS GOODS CERTIFICATE", "CITES CERTIFICATE", "CARGO MANIFEST", "INVOICE", "HEALTH CERTIFICATE","PACKING LIST","CERTIFICATE OF ORIGIN","NEPPEX","OTHER"]] = Field(

        # set the extraction model based on the inferred document type
        extraction_model = None
        if LLM_inferred_document_type == 'AIRWAY BILL':
            extraction_model = get_instructor_class('Airway_bill')
        elif LLM_inferred_document_type == 'PHYTOSANITARY CERTIFICATE':
            extraction_model = get_instructor_class('Phytosanitary_certificate')
        elif LLM_inferred_document_type == 'NEPPEX':
            extraction_model = get_instructor_class('NEPPEX')
        elif LLM_inferred_document_type == 'CITES CERTIFICATE':
            extraction_model = get_instructor_class('CITES_certificate')
        elif LLM_inferred_document_type == 'PACKING LIST':
            extraction_model = get_instructor_class('Packing_list')
        elif LLM_inferred_document_type == 'INVOICE':
            extraction_model = get_instructor_class('Invoice')
        # elif LLM_inferred_document_type == 'DANGEROUS GOODS CERTIFICATE':
        #     extraction_model = Dangerous_goods_certificate
        
        input_dict_document_master['document_types_detected'] = list(set(input_dict_document_master['document_types_detected'] + [LLM_inferred_document_type]))
        if LLM_inferred_document_type in ['AIRWAY BILL', 'PHYTOSANITARY CERTIFICATE', 'NEPPEX','CITES CERTIFICATE', 'PACKING LIST', 'INVOICE']:
            # create a new `LLM_visual_airway_bill` key in the dictionary for the analyzed document, which will contain the LLM response with the extracted information
            input_dict_document_master['input_image_list'][index_document_entity]['LLM_visual_extracted_details'] = {}

            # call the LLM model to extract the required information from the document, get back the instructor object
            input_prompt = f"Analyze this document using both the image and OCR data of the image provided. Use JSON tool to extract the needed information and label the required fields. \n\n # OCR DATA: \n\n {doc_ocr_result_obj.content}"

            LLM_response_instructor_object = LLM_visual_call(extraction_model, base64_document_page_for_analysis, input_prompt)

            # track token usage
            input_dict_document_master['total_tokens_combined'] += LLM_response_instructor_object._raw_response.usage.model_dump()['total_tokens']
            input_dict_document_master['total_tokens_completion'] += LLM_response_instructor_object._raw_response.usage.model_dump()['completion_tokens']
            input_dict_document_master['total_tokens_prompt'] += LLM_response_instructor_object._raw_response.usage.model_dump()['prompt_tokens']
            
            # convert the instructor object to a dictionary
            LLM_response_dict = LLM_response_instructor_object.model_dump()

            # add the extracted information to the dictionary
            input_dict_document_master['input_image_list'][index_document_entity]['LLM_visual_extracted_details'] = LLM_response_dict

            if LLM_inferred_document_type == 'AIRWAY BILL':
                input_dict_document_master['input_image_list'][index_document_entity]['LLM_visual_extracted_details']['airway_bill_id'] = input_dict_document_master['input_image_list'][index_document_entity]['LLM_visual_extracted_details']['airway_bill_id'].replace("|", "")
                input_dict_document_master['input_image_list'][index_document_entity]['LLM_visual_extracted_air_carrier'] = LLM_response_dict['air_carrier_label'][0]
                
                # set the master AWB carrier if it is not set
                if input_dict_document_master['master_awb_carrier'] == "":
                    input_dict_document_master['master_awb_carrier'] = LLM_response_dict['air_carrier_label'][0]

            # Notify progress after extracting details
            callback_dict_extraction = input_dict_document_master['input_image_list'][index_document_entity]
            if progress_callback:
                progress_callback(callback_dict_extraction, f"extraction")

    input_dict_document_master['document_extracted_markdown'] = aggregate_documents_to_markdown(input_dict_document_master)
    input_dict_document_master['validation_rules'] = compile_validation_rules(input_dict_document_master)
    input_dict_document_master['validation_rules'] = validate_document_package(input_dict_document_master)

    # check if any validation rules failed and set final status
    markdown_validation_result, final_validated_passed_check = aggregate_validation_to_markdown(input_dict_document_master)
    input_dict_document_master['validation_result_markdown'] = markdown_validation_result
    input_dict_document_master['final_validated_passed_check'] = final_validated_passed_check
    final_markdown =  input_dict_document_master['validation_result_markdown'] + input_dict_document_master['document_extracted_markdown']

    # Notify progress after final validations
    callback_dict_validation = input_dict_document_master
    if progress_callback:
        progress_callback(callback_dict_validation, f"validation")
    
    end_time = time.time()
    processing_time = end_time - start_time
    input_dict_document_master['processing_time'] = processing_time

    return input_dict_document_master

def compile_validation_rules(input_dict_document_master: dict):
    rules_dict = {
        "fundamental_rules": []
        ,"situation_specific_rules": []
        ,"carrier_rules": []
    }

    # set fundamental rules
    awb_exists_check = {
        "rule_name": "AWB exists",
        "rule_origin": "IATA",
        "rule_description": "The Airway Bill must exist in the document set",
        "rule_validation_status": "PENDING",
        "rule_validation_result_comment": "",
    }
    rules_dict['fundamental_rules'].append(awb_exists_check)

    awb_extracted_check = {
        "rule_name": "AWB ID provided",
        "rule_origin": "IATA",
        "rule_description": "Every Airway Bill should have an airway bill ID available and extracted",
        "rule_validation_status": "PENDING", 
        "rule_validation_result_comment": ""
    }
    rules_dict['fundamental_rules'].append(awb_extracted_check)

    country_of_origin_check = {
        "rule_name": "Country of Origin provided",
        "rule_origin": "IATA",
        "rule_description": "The country of origin should be provided on the airway bill document",
        "rule_validation_status": "PENDING",
        "rule_validation_result_comment": "",
    }
    rules_dict['fundamental_rules'].append(country_of_origin_check)

    country_of_destination_check = {
        "rule_name": "Country of Destination provided",
        "rule_origin": "IATA",
        "rule_description": "The country of destination should be provided on the airway bill document",
        "rule_validation_status": "PENDING",
        "rule_validation_result_comment": "",
    }
    rules_dict['fundamental_rules'].append(country_of_destination_check)

    # situation specific rules, based on AIRWAY BILL information
    # check for a need for dry ice, CITES and other conditions
    phytosanitary_certificate_required_check = None
    CITES_type_of_goods_check = None
    handling_muliple_temperature_band_check = None

    # set `Situation specific` rules based on Airway Bill
    for index, value in enumerate(input_dict_document_master['input_image_list']):
        document_type = input_dict_document_master['input_image_list'][index]['LLM_visual_document_type']
        
        # for AWB documents
        if document_type == 'AIRWAY BILL':
            #Dry ice check
            # if input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['dry_ice_usage_label'][0] == "USED":
            #     dry_ice_mentioned_in_awb_check = {
            #         "rule_name": "Dry ice dangeroud goods certificate required",
            #         "rule_origin": "IATA",
            #         "rule_description": "When dry ice is used for temperature control in perishable cargo, a dangeroud goods certificate should be included",
            #         "rule_validation_status": "PENDING",
            #         "rule_validation_result_comment": "",
            #     }
            #     rules_dict['situation_specific_rules'].append(dry_ice_mentioned_in_awb_check)

            #CITES check (Convention on International Trade in Endangered Species of Wild Fauna and Flora)
            for cargo_item in input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['cargo_items_list']:
                
                #Check if the type of goods falls under CITES is applicable only to live animals and plants/flowers     
                if cargo_item['perishible_cargo_type'][0] in ["FLOWERS", "OTHER PLANTS", "LIVE ANIMALS"]:
                    cites_item_check_class = get_instructor_class('CITES_items_check')
                    markdown_document_extracted = input_dict_document_master['document_extracted_markdown']
                    rule_description = "When perishable goods potentially fall under CITES, a further check should be performed if the goods transported and described in the documentation set are part of the CITES list and whether a CITES certificate is required"

                    # call the LLM model to check if the items are part of the CITES list (list is hardcoded), get back the instructor object
                    LLM_response_instructor_object = LLM_text_call(cites_item_check_class, markdown_document_extracted, f"Use JSON tool to perform validation, {rule_description}")

                    # track token usage
                    input_dict_document_master['total_tokens_combined'] += LLM_response_instructor_object._raw_response.usage.model_dump()['total_tokens']
                    input_dict_document_master['total_tokens_completion'] += LLM_response_instructor_object._raw_response.usage.model_dump()['completion_tokens']
                    input_dict_document_master['total_tokens_prompt'] += LLM_response_instructor_object._raw_response.usage.model_dump()['prompt_tokens']
            

                    # convert the instructor object to a dictionary
                    LLM_response_dict = LLM_response_instructor_object.model_dump()

                    if LLM_response_dict['cites_status_check'][0] == "CITES_DETECTED":
                        CITES_type_of_goods_check = {
                            "rule_name": "CITES certificate required",
                            "rule_origin": "IATA",
                            "rule_description": "When perishable goods that fall under CITES are detected in the document set, we need to verify that the CITES certificate is present as part of the document set",
                            "rule_validation_status": "PENDING",
                            "rule_validation_result_comment": f"CITES rule detection trigger expalantion: {LLM_response_dict['cites_status_check_explanation']}",
                        }
                        rules_dict['situation_specific_rules'].append(CITES_type_of_goods_check)

                        CITES_certificate_info_awb_match_check = {
                            "rule_name": "CITES certificate info match to AWB required",
                            "rule_origin": "IATA",
                            "rule_description": "CITES certificate information should match the information on the Airway Bill",
                            "rule_validation_status": "PENDING",
                            "rule_validation_result_comment": "",
                        }
                        rules_dict['situation_specific_rules'].append(CITES_certificate_info_awb_match_check)
                
            if cargo_item['perishible_cargo_type'][0] in ["FRESH PRODUCE", "FLOWERS", "OTHER PLANTS"]:
                phytosanitary_certificate_required_check = {
                    "rule_name": "Phytosanitary certificate required",
                    "rule_origin": "IATA",
                    "rule_description": "Phytosanitary certificate is required when either FRESH PRODUCE, FLOWERS or OTHER PLANTS are detected in the Airway Bill. This is an assumption in scope of the POC",
                    "rule_validation_status": "PENDING",
                    "rule_validation_result_comment": f"Cargo item type detected which triggered the rule: {cargo_item['perishible_cargo_type'][0]}",
                }
                rules_dict['situation_specific_rules'].append(phytosanitary_certificate_required_check)

                phytosanitary_certificate_info_awb_match_check = {
                    "rule_name": "Phytosanitary certificate info match to AWB required",
                    "rule_origin": "IATA",
                    "rule_description": "Phytosanity certificate information should match the information on the Airway Bill.",
                    "rule_validation_status": "PENDING",
                    "rule_validation_result_comment": "",
                }
                rules_dict['situation_specific_rules'].append(phytosanitary_certificate_info_awb_match_check)

            if cargo_item['perishible_cargo_type'][0] in ["SEAFOOD"] and input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['country_of_origin_label'].lower() == "chile":
                neppex_chile_certificate_required_check = {
                    "rule_name": "NEPPEX certificate required for seafood Chile export",
                    "rule_origin": "Chile export regulations",
                    "rule_description": "NEPPEX certificate is required for salmon when it is exported from Chile as per information obtained from LATAM operator in the scope of the POC (Excel file)",
                    "rule_validation_status": "PENDING",
                    "rule_validation_result_comment": "",
                }
                rules_dict['situation_specific_rules'].append(neppex_chile_certificate_required_check)

                neppex_chile_certificate_info_awb_match_check = {
                    "rule_name": "NEPPEX certificate information must match Airway Bill",
                    "rule_origin": "Chile export regulations",
                    "rule_description": "The information on the NEPPEX certificate should match the information on the Airway Bill, specifically country of origin, destination and items transported. NEPPEX certificate is required for seafood Chile export as per information obtained from LATAM operator in the scope of the POC (Excel file)",
                    "rule_validation_status": "PENDING",
                    "rule_validation_result_comment": "",
                }
                rules_dict['situation_specific_rules'].append(neppex_chile_certificate_info_awb_match_check)

            
            # if input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['handling_temperature_band_check'][0] == 'MULTIPLE':
            #     handling_muliple_temperature_band_check = {
            #             "rule_name": "Multiple temperature bands mentioned in the handling instructions",
            #             "rule_origin": "IATA (LATAM section)",
            #             "rule_description": "IATA PCR 24 regulation, section 3.1 for LATAM operator states that when multiple temperature bands are mentioned in the handling requirement of the airway bill, the cargo will not be shipped and put `ON HOLD` instead.", 
            #             "rule_validation_status": "FAILED",
            #             "rule_validation_result_comment": f"Multiple temperature bands mentioned in the handling instructions: {input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['handling_temperature_band_check_explanation']}",
            #         }
            #     rules_dict['situation_specific_rules'].append(handling_muliple_temperature_band_check)


    # set `carrier specific` rules
    # ANA carrier rules
    if input_dict_document_master['master_awb_carrier'] == 'ALL NIPPON AIRWAYS':
        # ANA aleays requires a packing list
        packing_list_required_check = {
                    "rule_name": "ANA packing list required",
                    "rule_origin": "ANA internal regulations",
                    "rule_description": "Valid packing list document is required as part of the export document set by ANA",
                    "rule_validation_status": "PENDING",
                    "rule_validation_result_comment": "",
                }
        rules_dict['carrier_rules'].append(packing_list_required_check)

        packing_list_info_awb_match_check = {
            "rule_name": "Packing list information must match Airway Bill",
            "rule_origin": "ANA internal regulations",
            "rule_description": "The information on the packing list should match the information on the Airway Bill, specifically country of origin, destination and items transported.",
            "rule_validation_status": "PENDING",
            "rule_validation_result_comment": "",
        }
        rules_dict['carrier_rules'].append(packing_list_info_awb_match_check)
        
        # ANA aleays requires an invoice
        invoice_required_check = {
                    "rule_name": "ANA invoice required",
                    "rule_origin": "ANA internal regulations",
                    "rule_description": "Valid invoice document is required as part of the export document set by ANA",
                    "rule_validation_status": "PENDING",
                    "rule_validation_result_comment": "",
                }
        rules_dict['carrier_rules'].append(invoice_required_check)

        invoice_info_awb_match_check = {
            "rule_name": "ANA Invoice information must match Airway Bill",
            "rule_origin": "ANA internal regulations",
            "rule_description": "The information on invoice should match the information on the Airway Bill, specifically country of origin and items transported.",
            "rule_validation_status": "PENDING",
            "rule_validation_result_comment": "",
        }
        rules_dict['carrier_rules'].append(invoice_info_awb_match_check)
    
    
    if input_dict_document_master['master_awb_carrier'] == 'LATAM':
        
        # Loop through the documents
        for index, value in enumerate(input_dict_document_master['input_image_list']):
            document_type = input_dict_document_master['input_image_list'][index]['LLM_visual_document_type']
            
            # for AWB document
            if document_type == 'AIRWAY BILL':
                
                # if seafood, LATAM requires a phytosanitary certificate (normally it is required for plants only)
                if cargo_item['perishible_cargo_type'][0] in ["SEAFOOD"]:
                    phytosanitary_certificate_required_check = {
                        "rule_name": "LATAM phytosanitary certificate required for seafood",
                        "rule_origin": "LATAM internal regulations",
                        "rule_description": "LATAM requires a Phytosanitary certificate when SEAFOOD is detected on the Airway Bill.",
                        "rule_validation_status": "PENDING",
                        "rule_validation_result_comment": f"Cargo item type detected which triggered the rule: {cargo_item['perishible_cargo_type'][0]}",
                    }
                    rules_dict['carrier_rules'].append(phytosanitary_certificate_required_check)

                    phytosanitary_certificate_info_awb_match_check = {
                        "rule_name": "LATAM seafood phytosanitary certificate info match to AWB required",
                        "rule_origin": "LATAM internal regulations",
                        "rule_description": "Phytosanity certificate information should match the information on the Airway Bill.",
                        "rule_validation_status": "PENDING",
                        "rule_validation_result_comment": "",
                    }
                    rules_dict['carrier_rules'].append(phytosanitary_certificate_info_awb_match_check)

    return rules_dict

def validate_document_package(input_dict_document_master: dict):
    
    rules_dict = input_dict_document_master['validation_rules']

    # validate the document submission using the fundamental rules
    for fundamental_rule in rules_dict['fundamental_rules']:
        if fundamental_rule['rule_name'] == "AWB exists":
            if 'AIRWAY BILL' in  input_dict_document_master['document_types_detected']:
                fundamental_rule['rule_validation_status'] = "PASSED"
                fundamental_rule['rule_validation_result_comment'] = "An Airway bill was detected in the document set"
            else:
                fundamental_rule['rule_validation_status'] = "FAILED"
                fundamental_rule['rule_validation_result_comment'] = "No Airway bill detected in the document set"

        if fundamental_rule['rule_name'] == "AWB ID provided":
            for index, value in enumerate(input_dict_document_master['input_image_list']):
                # only check the Airway Bill documents
                if input_dict_document_master['input_image_list'][index]["LLM_visual_document_type"] == 'AIRWAY BILL':
                    if input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['airway_bill_id'] != "":
                        fundamental_rule['rule_validation_status'] = "PASSED"
                        fundamental_rule['rule_validation_result_comment'] = "Airway bill ID was detected on the Airway Bill document(s)"
                    else:
                        fundamental_rule['rule_validation_status'] = "FAILED"
                        fundamental_rule['rule_validation_result_comment'] = f"Airway Bill in document {input_dict_document_master['input_image_list'][index]['document_entity_name']} did not have a valid Airway Bill ID extracted"
                        break
        
        if fundamental_rule['rule_name'] == "Country of Origin provided":
            for index, value in enumerate(input_dict_document_master['input_image_list']):
                if input_dict_document_master['input_image_list'][index]["LLM_visual_document_type"] == 'AIRWAY BILL':
                    if input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['country_of_origin_label'] != "":
                        fundamental_rule['rule_validation_status'] = "PASSED"
                        fundamental_rule['rule_validation_result_comment'] = "Country of Origin was detected on the Airway Bill document(s)"
                    else:
                        fundamental_rule['rule_validation_status'] = "FAILED"
                        fundamental_rule['rule_validation_result_comment'] = f"Airway Bill in document {input_dict_document_master['input_image_list'][index]['document_entity_name']} did not have a valid Country of Origin extracted"
                        break
        
        if fundamental_rule['rule_name'] == "Country of Destination provided":
            for index, value in enumerate(input_dict_document_master['input_image_list']):
                if input_dict_document_master['input_image_list'][index]["LLM_visual_document_type"] == 'AIRWAY BILL':
                    if input_dict_document_master['input_image_list'][index]['LLM_visual_extracted_details']['country_of_destination_label'] != "":
                        fundamental_rule['rule_validation_status'] = "PASSED"
                        fundamental_rule['rule_validation_result_comment'] = "Country of Destination was detected on the Airway Bill document(s)"
                    else:
                        fundamental_rule['rule_validation_status'] = "FAILED"
                        fundamental_rule['rule_validation_result_comment'] = f"Airway Bill in document {input_dict_document_master['input_image_list'][index]['document_entity_name']} did not have a valid Country of Destination extracted"
                        break
    
    # validate the document submission using the situation specific rules
    for situation_specific_rule in rules_dict['situation_specific_rules']:

        # validate the presence of the CITES certificate
        if situation_specific_rule['rule_name'] == "CITES certificate required":
            if 'CITES CERTIFICATE' in  input_dict_document_master['document_types_detected']:
                situation_specific_rule['rule_validation_status'] = "PASSED"
                situation_specific_rule['rule_validation_result_comment'] = situation_specific_rule['rule_validation_result_comment'] + "  CITES certificate was detected in the document set"
            else:
                situation_specific_rule['rule_validation_status'] = "FAILED"
                situation_specific_rule['rule_validation_result_comment'] = situation_specific_rule['rule_validation_result_comment'] + "  No CITES certificate detected in the document set"

        # validate the CITES certificate information against the Airway Bill information (if CITES certificate exists in the document set)
        if situation_specific_rule['rule_name'] == "CITES certificate info match to AWB required" and 'CITES CERTIFICATE' in  input_dict_document_master['document_types_detected']:
            
            # compile the info for the call to the LLM model to validate the CITES certificate information against the Airway Bill information
            validate_cites_certificate_class = get_instructor_class('validate_CITES_certificate')
            markdown_document_extracted = input_dict_document_master['document_extracted_markdown']
            # 'rule_validation_result_comment' include the cargo items which were tagged as requiring CITES certificate
            rule_description = situation_specific_rule['rule_validation_result_comment']

            # make the actual call to the LLM, to validate the CITES certificate information against the Airway Bill information
            LLM_response_instructor_object = LLM_text_call(validate_cites_certificate_class, markdown_document_extracted, f"Use JSON tool to perform validation, {rule_description}")

            # track token usage
            input_dict_document_master['total_tokens_combined'] += LLM_response_instructor_object._raw_response.usage.model_dump()['total_tokens']
            input_dict_document_master['total_tokens_completion'] += LLM_response_instructor_object._raw_response.usage.model_dump()['completion_tokens']
            input_dict_document_master['total_tokens_prompt'] += LLM_response_instructor_object._raw_response.usage.model_dump()['prompt_tokens']
            
            # convert the instructor object to a dictionary
            LLM_response_dict = LLM_response_instructor_object.model_dump()

            if LLM_response_dict['validation_status'][0] == "PASSED":
                situation_specific_rule['rule_validation_status'] = "PASSED"
                situation_specific_rule['rule_validation_result_comment'] = f"CITES Certificate information matches the Airway Bill information, {LLM_response_dict['validation_status_explanation']}"
            else:
                situation_specific_rule['rule_validation_status'] = "FAILED"
                situation_specific_rule['rule_validation_result_comment'] = f"CITES Certificate information does not match the Airway Bill information, {LLM_response_dict['validation_status_explanation']}"  

        # check if phytosanitary certificate is required
        if situation_specific_rule['rule_name'] == "Phytosanitary certificate required":
            if 'PHYTOSANITARY CERTIFICATE' in  input_dict_document_master['document_types_detected']:
                situation_specific_rule['rule_validation_status'] = "PASSED"
                situation_specific_rule['rule_validation_result_comment'] = "Phytosanitary Certificate was detected in the document set"
            else:
                situation_specific_rule['rule_validation_status'] = "FAILED"
                situation_specific_rule['rule_validation_result_comment'] = "Phytosanitary Certificate was not detected in the document set"
        
        # if the phytosanitary certificate is required, check if the information matches the Airway Bill information
        if situation_specific_rule['rule_name'] == "Phytosanitary certificate info match to AWB required" and 'PHYTOSANITARY CERTIFICATE' in  input_dict_document_master['document_types_detected']:
            
            # compile the info for the call to the LLM model to validate the phytosanitary certificate information against the Airway Bill information
            
            if input_dict_document_master['master_awb_carrier'] == 'QATAR AIRWAYS':
                validate_phytosanitary_certificate_class = get_instructor_class('validate_phytosanitary_certificate_qatar')
            else:
                validate_phytosanitary_certificate_class = get_instructor_class('validate_phytosanitary_certificate')
            
            markdown_document_extracted = input_dict_document_master['document_extracted_markdown']
            rule_description = situation_specific_rule['rule_description']

            # make the actual call to the LLM, to validate the phytosanitary certificate information against the Airway Bill information
            LLM_response_instructor_object = LLM_text_call(validate_phytosanitary_certificate_class, markdown_document_extracted, f"Use JSON tool to perform validation, {rule_description}")
            
            # track token usage
            input_dict_document_master['total_tokens_combined'] += LLM_response_instructor_object._raw_response.usage.model_dump()['total_tokens']
            input_dict_document_master['total_tokens_completion'] += LLM_response_instructor_object._raw_response.usage.model_dump()['completion_tokens']
            input_dict_document_master['total_tokens_prompt'] += LLM_response_instructor_object._raw_response.usage.model_dump()['prompt_tokens']
            
            # convert the instructor object to a dictionary
            LLM_response_dict = LLM_response_instructor_object.model_dump()

            if LLM_response_dict['validation_status'][0] == "PASSED":
                situation_specific_rule['rule_validation_status'] = "PASSED"
                situation_specific_rule['rule_validation_result_comment'] = f"Phytosanitary Certificate information matches the Airway Bill information, {LLM_response_dict['validation_status_explanation']}"
            else:
                situation_specific_rule['rule_validation_status'] = "FAILED"

                markdown_validation_fail_details = ""

                for validation_issue in LLM_response_dict['validation_issues']:
                    markdown_validation_fail_details += f":heavy_exclamation_mark: {validation_issue['validation_issue_description']} \n\n"

                situation_specific_rule['rule_validation_result_comment'] = f"Phytosanitary Certificate information does not match the Airway Bill information, {LLM_response_dict['validation_status_explanation']}\n\n {markdown_validation_fail_details}"
        
        
        if situation_specific_rule['rule_name'] == "NEPPEX certificate required for seafood Chile export":
            if 'NEPPEX' in  input_dict_document_master['document_types_detected']:
                situation_specific_rule['rule_validation_status'] = "PASSED"
                situation_specific_rule['rule_validation_result_comment'] = "NEPPEX Certificate was detected in the document set"
            else:
                situation_specific_rule['rule_validation_status'] = "FAILED"
                situation_specific_rule['rule_validation_result_comment'] = "NEPPEX Certificate was not detected in the document set"
        
        if situation_specific_rule['rule_name'] == "NEPPEX certificate information must match Airway Bill" and 'NEPPEX' in  input_dict_document_master['document_types_detected']:
            
            # compile the info for the call to the LLM model to validate the NEPPEX certificate information against the Airway Bill information
            validate_neppex_certificate_class = get_instructor_class('validate_NEPPEX_certificate')
            markdown_document_extracted = input_dict_document_master['document_extracted_markdown']
            rule_description = situation_specific_rule['rule_description']

            # make the actual call to the LLM, to validate the NEPPEX certificate information against the Airway Bill information
            LLM_response_instructor_object = LLM_text_call(validate_neppex_certificate_class, markdown_document_extracted, f"Use JSON tool to perform validation, {rule_description}")

            # track token usage
            input_dict_document_master['total_tokens_combined'] += LLM_response_instructor_object._raw_response.usage.model_dump()['total_tokens']
            input_dict_document_master['total_tokens_completion'] += LLM_response_instructor_object._raw_response.usage.model_dump()['completion_tokens']
            input_dict_document_master['total_tokens_prompt'] += LLM_response_instructor_object._raw_response.usage.model_dump()['prompt_tokens']
            

            # convert the instructor object to a dictionary
            LLM_response_dict = LLM_response_instructor_object.model_dump()

            if LLM_response_dict['validation_status'][0] == "PASSED":
                situation_specific_rule['rule_validation_status'] = "PASSED"
                situation_specific_rule['rule_validation_result_comment'] = f"NEPPEX Certificate information matches the Airway Bill information, {LLM_response_dict['validation_status_explanation']}"
            else:
                situation_specific_rule['rule_validation_status'] = "FAILED"
                situation_specific_rule['rule_validation_result_comment'] = f"NEPPEX Certificate information does not match the Airway Bill information, {LLM_response_dict['validation_status_explanation']}"

        # if situation_specific_rule['rule_name'] == "Dry ice dangeroud goods certificate required":
        #     if 'DANGEROUS GOODS CERTIFICATE' in  input_dict_document_master['document_types_detected']:
        #         fundamental_rule['rule_validation_status'] = "PASSED"
        #         fundamental_rule['rule_validation_result_comment'] = "A Dangerous Goods Certificate was detected in the document set, which is needed for dry ice usage in temperature control"
        #     else:
        #         fundamental_rule['rule_validation_status'] = "FAILED"
        #         fundamental_rule['rule_validation_result_comment'] = "No Dangerous Goods Certificate detected in the document set. Dry ice usage in temperature control requires a Dangerous Goods Certificate"
    
    for carrier_rule in rules_dict['carrier_rules']:
        # ANA -- validate the presence of the packing list
        if carrier_rule['rule_name'] == "ANA packing list required":
            if 'PACKING LIST' in  input_dict_document_master['document_types_detected']:
                carrier_rule['rule_validation_status'] = "PASSED"
                carrier_rule['rule_validation_result_comment'] = carrier_rule['rule_validation_result_comment'] + "  Packing List document was detected in the document set"
            else:
                carrier_rule['rule_validation_status'] = "FAILED"
                carrier_rule['rule_validation_result_comment'] = carrier_rule['rule_validation_result_comment'] + "  Packing List document is missing from the document set"

        # ANA --if the packing list is required, check if the information matches the Airway Bill information
        if carrier_rule['rule_name'] == "Packing list information must match Airway Bill" and 'PACKING LIST' in  input_dict_document_master['document_types_detected']:

            # compile the info for the call to the LLM model to validate the packing list information against the Airway Bill information
            validate_document_class = get_instructor_class('validate_packing_list')
            markdown_document_extracted = input_dict_document_master['document_extracted_markdown']
            rule_description = carrier_rule['rule_description']

            # make the actual call to the LLM, to validate the packing list information against the Airway Bill information
            LLM_response_instructor_object = LLM_text_call(validate_document_class, markdown_document_extracted, f"Use JSON tool to perform validation, {rule_description}")
            
            # track token usage
            input_dict_document_master['total_tokens_combined'] += LLM_response_instructor_object._raw_response.usage.model_dump()['total_tokens']
            input_dict_document_master['total_tokens_completion'] += LLM_response_instructor_object._raw_response.usage.model_dump()['completion_tokens']
            input_dict_document_master['total_tokens_prompt'] += LLM_response_instructor_object._raw_response.usage.model_dump()['prompt_tokens']
            
            # convert the instructor object to a dictionary
            LLM_response_dict = LLM_response_instructor_object.model_dump()

            if LLM_response_dict['validation_status'][0] == "PASSED":
                carrier_rule['rule_validation_status'] = "PASSED"
                carrier_rule['rule_validation_result_comment'] = "Packing list information matches the Airway Bill information"
            else:
                carrier_rule['rule_validation_status'] = "FAILED"

                markdown_validation_fail_details = ""

                for validation_issue in LLM_response_dict['validation_issues']:
                    markdown_validation_fail_details += f":heavy_exclamation_mark: {validation_issue['validation_issue_description']} \n\n"

                carrier_rule['rule_validation_result_comment'] = f"Packing list information does not match the Airway Bill information, {LLM_response_dict['validation_status_explanation']}\n\n {markdown_validation_fail_details}"
        
        # ANA -- validate the presence of the invoice
        if carrier_rule['rule_name'] == "ANA invoice required":
            if 'INVOICE' in  input_dict_document_master['document_types_detected']:
                carrier_rule['rule_validation_status'] = "PASSED"
                carrier_rule['rule_validation_result_comment'] = carrier_rule['rule_validation_result_comment'] + "  Invoice document was detected in the document set"
            else:
                carrier_rule['rule_validation_status'] = "FAILED"
                carrier_rule['rule_validation_result_comment'] = carrier_rule['rule_validation_result_comment'] + "  Invoice document is missing from the document set"

        # ANA -- if the invoice is required, check if the information matches the Airway Bill information
        if carrier_rule['rule_name'] == "ANA Invoice information must match Airway Bill" and 'INVOICE' in input_dict_document_master['document_types_detected']:

            # compile the info for the call to the LLM model to validate the invoice information against the Airway Bill information
            validate_document_class = get_instructor_class('validate_packing_list')
            markdown_document_extracted = input_dict_document_master['document_extracted_markdown']
            rule_description = carrier_rule['rule_description']

            # make the actual call to the LLM, to validate the invoice information against the Airway Bill information
            LLM_response_instructor_object = LLM_text_call(validate_document_class, markdown_document_extracted, f"Use JSON tool to perform validation, {rule_description}")
            
            # track token usage
            input_dict_document_master['total_tokens_combined'] += LLM_response_instructor_object._raw_response.usage.model_dump()['total_tokens']
            input_dict_document_master['total_tokens_completion'] += LLM_response_instructor_object._raw_response.usage.model_dump()['completion_tokens']
            input_dict_document_master['total_tokens_prompt'] += LLM_response_instructor_object._raw_response.usage.model_dump()['prompt_tokens']
            
            # convert the instructor object to a dictionary
            LLM_response_dict = LLM_response_instructor_object.model_dump()

            if LLM_response_dict['validation_status'][0] == "PASSED":
                carrier_rule['rule_validation_status'] = "PASSED"
                carrier_rule['rule_validation_result_comment'] = "Invoice information matches the Airway Bill information"
            else:
                carrier_rule['rule_validation_status'] = "FAILED"

                markdown_validation_fail_details = ""

                for validation_issue in LLM_response_dict['validation_issues']:
                    markdown_validation_fail_details += f":heavy_exclamation_mark: {validation_issue['validation_issue_description']} \n\n"

                carrier_rule['rule_validation_result_comment'] = f"Invoice information does not match the Airway Bill information, {LLM_response_dict['validation_status_explanation']}\n\n {markdown_validation_fail_details}"

        # validate the presence of the Phytosantiry
        if carrier_rule['rule_name'] == "LATAM phytosanitary certificate required for seafood":
            if 'PHYTOSANITARY CERTIFICATE' in  input_dict_document_master['document_types_detected']:
                carrier_rule['rule_validation_status'] = "PASSED"
                carrier_rule['rule_validation_result_comment'] = carrier_rule['rule_validation_result_comment'] + "  phytosanitary certificate was detected in the document set"
            else:
                carrier_rule['rule_validation_status'] = "FAILED"
                carrier_rule['rule_validation_result_comment'] = carrier_rule['rule_validation_result_comment'] + "  phytosanitary certificate is missing from the document set"


        # if the phytosanitary certificate is required, check if the information matches the Airway Bill information
        if carrier_rule['rule_name'] == "LATAM seafood phytosanitary certificate info match to AWB required" and 'PHYTOSANITARY CERTIFICATE' in  input_dict_document_master['document_types_detected']:
            
            # compile the info for the call to the LLM model to validate the phytosanitary certificate information against the Airway Bill information
            validate_phytosanitary_certificate_class = get_instructor_class('validate_phytosanitary_certificate')
            
            markdown_document_extracted = input_dict_document_master['document_extracted_markdown']
            rule_description = carrier_rule['rule_description']

            # make the actual call to the LLM, to validate the phytosanitary certificate information against the Airway Bill information
            LLM_response_instructor_object = LLM_text_call(validate_phytosanitary_certificate_class, markdown_document_extracted, f"Use JSON tool to perform validation, {rule_description}")
            
            # track token usage
            input_dict_document_master['total_tokens_combined'] += LLM_response_instructor_object._raw_response.usage.model_dump()['total_tokens']
            input_dict_document_master['total_tokens_completion'] += LLM_response_instructor_object._raw_response.usage.model_dump()['completion_tokens']
            input_dict_document_master['total_tokens_prompt'] += LLM_response_instructor_object._raw_response.usage.model_dump()['prompt_tokens']
            
            # convert the instructor object to a dictionary
            LLM_response_dict = LLM_response_instructor_object.model_dump()

            if LLM_response_dict['validation_status'][0] == "PASSED":
                carrier_rule['rule_validation_status'] = "PASSED"
                carrier_rule['rule_validation_result_comment'] = f"Phytosanitary Certificate information matches the Airway Bill information, {LLM_response_dict['validation_status_explanation']}"
            else:
                carrier_rule['rule_validation_status'] = "FAILED"

                markdown_validation_fail_details = ""

                for validation_issue in LLM_response_dict['validation_issues']:
                    markdown_validation_fail_details += f":heavy_exclamation_mark: {validation_issue['validation_issue_description']} \n\n"

                carrier_rule['rule_validation_result_comment'] = f"Phytosanitary Certificate information does not match the Airway Bill information, {LLM_response_dict['validation_status_explanation']}\n\n {markdown_validation_fail_details}"

    return rules_dict