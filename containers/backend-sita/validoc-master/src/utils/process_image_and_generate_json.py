import json
import os

def process_image_and_generate_json(image_path, from_whatsapp_number, user_context):
    """Process a single image, analyze it, validate results, and generate JSON."""
    results = []
    custom_prompt = 'Extract the following details from the provided Air Waybill (AWB) image. From Airport of Departure predict Exporting Country in Alpha-2 format. From Airport of Destination predict Importing Country in Alpha-2 format.Return a valid JSON object with the following structure. Return only this JSON object with no additional text: {  "WaybillNumber": "",  "Shipper Name": "",  "Shipper Address": "",  "Shipper Phone": "",  "Shipper Account Number": "",  "Consignee Name": "",  "Consignee Address": "",  "Consignee Phone": "",  "Consignee Account Number": "",  "Issuing Carrier Agent Name": "",  "Issuing Carrier Agent Address": "",  "Issuing Carrier Agent City": "",  "Agent IATA Code": "",  "Agent Account Number": "",  "Airport of Departure": "",  "Routing and Destination": "",  "Declared Value for Carriage": "",  "Declared Value for Customs": "",  "Airport of Destination": "",  "Amount of Insurance": "",  "Handling Information": "",  "Number of Pieces": "",  "Gross Weight": "",  "Weight Unit": "",  "Commodity Number": "",  "Chargeable Weight": "",  "Rate/Charge": "",  "Total": "",  "Nature and Quantity of Goods": "",  "Shipper/Agent Signature": "",  "Executed On": ""  "Requested Flight Date": "",  "Charge": "",  "ChargeCurrency": "",  "Prepaid Charges": "",  "Total Prepaid": "",  "Total Collect": "",  "Exporting Country": "",  "Importing Country": "",}'
    structured_data = {}
    raw_responses = []
    try:
        raw_response = analyze_image(image_path, custom_prompt)
        raw_responses.append(raw_response)
        extracted_data = {'WaybillNumber': extract_value(raw_response, 'WaybillNumber'), 'Shipper Name': extract_value(raw_response, 'Shipper Name'), 'Shipper Address': extract_value(raw_response, 'Shipper Address'), 'Shipper Phone': extract_value(raw_response, 'Shipper Phone'), 'Shipper Account Number': extract_value(raw_response, 'Shipper Account Number'), 'Consignee Name': extract_value(raw_response, 'Consignee Name'), 'Consignee Address': extract_value(raw_response, 'Consignee Address'), 'Consignee Phone': extract_value(raw_response, 'Consignee Phone'), 'Consignee Account Number': extract_value(raw_response, 'Consignee Account Number'), 'Issuing Carrier Agent Name': extract_value(raw_response, 'Issuing Carrier Agent Name'), 'Issuing Carrier Agent Address': extract_value(raw_response, 'Issuing Carrier Agent Address'), 'Issuing Carrier Agent City': extract_value(raw_response, 'Issuing Carrier Agent City'), 'Agent IATA Code': extract_value(raw_response, 'Agent IATA Code'), 'Agent Account Number': extract_value(raw_response, 'Agent Account Number'), 'Airport of Departure': extract_value(raw_response, 'Airport of Departure'), 'Routing and Destination': extract_value(raw_response, 'Routing and Destination'), 'Declared Value for Carriage': extract_value(raw_response, 'Declared Value for Carriage'), 'Declared Value for Customs': extract_value(raw_response, 'Declared Value for Customs'), 'Airport of Destination': extract_value(raw_response, 'Airport of Destination'), 'Amount of Insurance': extract_value(raw_response, 'Amount of Insurance'), 'Handling Information': extract_value(raw_response, 'Handling Information'), 'Number of Pieces': extract_value(raw_response, 'Number of Pieces'), 'Gross Weight': extract_value(raw_response, 'Gross Weight'), 'Weight Unit': extract_value(raw_response, 'Weight Unit'), 'Commodity Number': extract_value(raw_response, 'Commodity Number'), 'Chargeable Weight': extract_value(raw_response, 'Chargeable Weight'), 'Rate/Charge': extract_value(raw_response, 'Rate/Charge'), 'Total': extract_value(raw_response, 'Total'), 'Nature and Quantity of Goods': extract_value(raw_response, 'Nature and Quantity of Goods'), 'Shipper/Agent Signature': extract_value(raw_response, 'Shipper/Agent Signature'), 'Executed On': extract_value(raw_response, 'Executed On'), 'Requested Flight Date': extract_value(raw_response, 'Requested Flight Date'), 'Charge': extract_value(raw_response, 'Charge'), 'ChargeCurrency': extract_value(raw_response, 'ChargeCurrency'), 'Prepaid Charges': extract_value(raw_response, 'Prepaid Charges'), 'Total Prepaid': extract_value(raw_response, 'Total Prepaid'), 'Total Collect': extract_value(raw_response, 'Total Collect'), 'Exporting Country': extract_value(raw_response, 'Exporting Country'), 'Importing Country': extract_value(raw_response, 'Importing Country')}
        structured_data = {'document_details': {'awb_number': extracted_data.get('WaybillNumber', ''), 'shipper': {'name': extracted_data.get('Shipper Name', ''), 'address': extracted_data.get('Shipper Address', ''), 'phone': extracted_data.get('Shipper Phone', ''), 'account_number': extracted_data.get('Shipper Account Number', '')}, 'consignee': {'name': extracted_data.get('Consignee Name', ''), 'address': extracted_data.get('Consignee Address', ''), 'phone': extracted_data.get('Consignee Phone', ''), 'account_number': extracted_data.get('Consignee Account Number', '')}, 'issuing_carrier_agent': {'name': extracted_data.get('Issuing Carrier Agent Name'), 'address': extracted_data.get('Issuing Carrier Agent Address'), 'city': extracted_data.get('Issuing Carrier Agent City')}, 'iata_code': extracted_data.get('Agent IATA Code', ''), 'agent_account_number': extracted_data.get('Agent Account Number', ''), 'departure_airport': extracted_data.get('Airport of Departure', ''), 'routing_destination': extracted_data.get('Routing and Destination', ''), 'declared_value_carriage': extracted_data.get('Declared Value for Carriage', ''), 'declared_value_customs': extracted_data.get('Declared Value for Customs', ''), 'destination_airport': extracted_data.get('Airport of Destination', ''), 'insurance_amount': extracted_data.get('Amount of Insurance', ''), 'handling_info': extracted_data.get('Handling Information', ''), 'cargo': {'pieces': extracted_data.get('Number of Pieces', ''), 'weight': extracted_data.get('Gross Weight', ''), 'unit': extracted_data.get('Weight Unit', ''), 'commodity_number': extracted_data.get('Commodity Number', ''), 'chargeable_weight': extracted_data.get('Chargeable Weight', ''), 'rate': extracted_data.get('Rate/Charge', ''), 'total': extracted_data.get('Total', ''), 'description': extracted_data.get('Nature and Quantity of Goods', '')}, 'additional_details': {'requested_flight_date': extracted_data.get('Requested Flight Date', ''), 'charge': extracted_data.get('Charge', ''), 'charge_currency': extracted_data.get('ChargeCurrency', ''), 'prepaid_charges': extracted_data.get('Prepaid Charges', ''), 'total_prepaid': extracted_data.get('Total Prepaid', ''), 'total_collect': extracted_data.get('Total Collect', ''), 'exporting_country': extracted_data.get('Exporting Country', ''), 'importing_country': extracted_data.get('Importing Country', '')}, 'signature': extracted_data.get('Shipper/Agent Signature', ''), 'executed_on': extracted_data.get('Executed On', '')}}
        documents = load_document(regulations_folder_path)
        vector_store = create_vector_store(documents)
        retriever = vector_store.as_retriever()
        item_description = structured_data['document_details']['cargo']['description']
        query = f'What are the regulations for {item_description}?'
        relevant_sections = retriever.get_relevant_documents(query)
        structured_data['relevant_regulations'] = f'The items to be shipped are: {item_description}. ' + ' '.join((section.page_content for section in relevant_sections))
        missing_required, missing_optional = validate_document_details(structured_data['document_details'])
        structured_data['validation_status'] = 'success' if not missing_required else 'error'
        structured_data['missing_required_keys'] = missing_required
        structured_data['missing_optional_keys'] = missing_optional
        structured_data['extra_metadata'] = {'raw_responses': raw_responses}
        structured_data['exporting_country'] = extracted_data.get('Exporting Country', '')
        structured_data['importing_country'] = extracted_data.get('Importing Country', '')
        base_filename = f"{from_whatsapp_number.replace(':', '_').replace('+', '')}_{generate_unique_filename('doc', 'json').split('.')[0]}.json"
        output_json_path = os.path.join(output_folder, base_filename)
        with open(output_json_path, 'w') as json_file:
            json.dump(structured_data, json_file, indent=4)
        user_context['current_json_path'] = output_json_path
        logger.info(f'Results saved to {output_json_path}')
        if missing_required:
            results.append('❌ Missing required documents:')
            results.extend((f'- {key}' for key in missing_required))
        else:
            results.append('✅ All required documents are present.')
        if missing_optional:
            results.append('⚠️ Missing optional details:')
            results.extend((f'- {key}' for key in missing_optional))
        color = 'green' if not missing_required else 'red'
        return (results, color)
    except Exception as e:
        logger.error(f'Error processing image: {e}')
        return ([f'Error processing image: {e}'], 'red')

