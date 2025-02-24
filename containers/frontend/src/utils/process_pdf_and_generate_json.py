import json
import os

def process_pdf_and_generate_json(pdf_path):
    """Process PDF, analyze images, validate results, and save JSON."""
    image_paths = convert_pdf_to_images(pdf_path)
    if not image_paths:
        return (['Failed to process PDF: {pdf_path}'], 'red')
    results = []
    custom_prompt = 'Extract the following details from the provided Air Waybill (AWB) image. Return a valid JSON object with the following structure. Return only this JSON object with no additional text: {  "WaybillNumber": "",  "Shipper Name": "",  "Shipper Address": "",  "Shipper Phone": "",  "Consignee Name": "",  "Consignee Address": "",  "Consignee Phone": "",  "Issuing Carrier Agent Name": "",  "Issuing Carrier Agent Address": "",  "Issuing Carrier Agent Phone": "",  "Requested Flight Date": "",  "NoOfPieces": "",  "Weight": "",  "Charge": "",  "NatureOfGoods": "",  "WeightUnit": "",  "ChargeCurrency": "",  "Prepaid Charges": "",  "Total Prepaid": "",  "Total Collect": ""}'
    structured_data = {}
    raw_responses = []
    for image_path in image_paths:
        raw_response = analyze_image(image_path, custom_prompt)
        raw_responses.append(raw_response)
        try:
            extracted_data = {'WaybillNumber': extract_value(raw_response, 'WaybillNumber'), 'Shipper Name': extract_value(raw_response, 'Shipper Name'), 'Shipper Address': extract_value(raw_response, 'Shipper Address'), 'Shipper Phone': extract_value(raw_response, 'Shipper Phone'), 'Consignee Name': extract_value(raw_response, 'Consignee Name'), 'Consignee Address': extract_value(raw_response, 'Consignee Address'), 'Consignee Phone': extract_value(raw_response, 'Consignee Phone'), 'Issuing Carrier Agent Name': extract_value(raw_response, 'Issuing Carrier Agent Name'), 'Issuing Carrier Agent Address': extract_value(raw_response, 'Issuing Carrier Agent Address'), 'Issuing Carrier Agent Phone': extract_value(raw_response, 'Issuing Carrier Agent Phone'), 'Requested Flight Date': extract_value(raw_response, 'Requested Flight Date'), 'NoOfPieces': extract_value(raw_response, 'NoOfPieces'), 'Weight': extract_value(raw_response, 'Weight'), 'Charge': extract_value(raw_response, 'Charge'), 'NatureOfGoods': extract_value(raw_response, 'NatureOfGoods'), 'WeightUnit': extract_value(raw_response, 'WeightUnit'), 'ChargeCurrency': extract_value(raw_response, 'ChargeCurrency'), 'Prepaid Charges': extract_value(raw_response, 'Prepaid Charges'), 'Total Prepaid': extract_value(raw_response, 'Total Prepaid'), 'Total Collect': extract_value(raw_response, 'Total Collect')}
            structured_data = {'document_details': {'awb_number': extracted_data.get('WaybillNumber', ''), 'shipper': {'name': extracted_data.get('Shipper Name', ''), 'address': extracted_data.get('Shipper Address', ''), 'phone': extracted_data.get('Shipper Phone', '')}, 'consignee': {'name': extracted_data.get('Consignee Name', ''), 'address': extracted_data.get('Consignee Address', ''), 'phone': extracted_data.get('Consignee Phone', '')}, 'issuing_carrier_agent': {'name': extracted_data.get('Issuing Carrier Agent Name', ''), 'address': extracted_data.get('Issuing Carrier Agent Address', ''), 'phone': extracted_data.get('Issuing Carrier Agent Phone', '')}, 'requested_flight_date': extracted_data.get('Requested Flight Date', ''), 'cargo': {'pieces': extracted_data.get('NoOfPieces', ''), 'weight': extracted_data.get('Weight', ''), 'unit': extracted_data.get('WeightUnit', ''), 'description': extracted_data.get('NatureOfGoods', '')}, 'charges': {'freight': extracted_data.get('Charge', ''), 'currency': extracted_data.get('ChargeCurrency', ''), 'prepaid': extracted_data.get('Prepaid Charges', ''), 'total_prepaid': extracted_data.get('Total Prepaid', ''), 'total_collect': extracted_data.get('Total Collect', '')}}}
            missing_required, missing_optional = validate_document_details(structured_data['document_details'])
            structured_data['validation_status'] = 'success' if not missing_required else 'error'
            structured_data['missing_required_keys'] = missing_required
            structured_data['missing_optional_keys'] = missing_optional
            results.append('Airway Bill validation successful.' if not missing_required else 'Airway Bill validation unsuccessful.')
        except Exception as e:
            structured_data['validation_status'] = 'error'
            structured_data['error_details'] = f'Error parsing response: {e}'
            results.append('Airway Bill validation unsuccessful.')
    structured_data['extra_metadata'] = {'processed_file': pdf_path, 'number_of_images': len(image_paths), 'raw_responses': raw_responses}
    output_json_path = os.path.join(output_folder, f'{os.path.basename(pdf_path)}.json')
    with open(output_json_path, 'w') as json_file:
        json.dump(structured_data, json_file, indent=4)
    print(f'Results saved to {output_json_path}')
    return (results, 'green' if 'successful' in results[0].lower() else 'red')

