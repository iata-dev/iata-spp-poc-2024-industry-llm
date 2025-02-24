from flask import Flask, request, render_template
import os
import requests
import shutil
import json

# Define Flask app
app = Flask(__name__)

# Store user contexts
user_contexts = {}  # A global dictionary to manage user-specific chat contexts

@app.route('/whatsapp', methods=['POST'])
def whatsapp_webhook():
    try:
        from_whatsapp_number = request.form.get('From')
        body = request.form.get('Body', '').strip().lower()
        media_url = request.form.get('MediaUrl0')
        media_content_type = request.form.get('MediaContentType0')
        if from_whatsapp_number not in user_contexts:
            user_contexts[from_whatsapp_number] = {'mode': 'awb', 'messages': [], 'requirements_message': None, 'uploaded_docs': [], 'document_analysis': [], 'awb_processed': False}
        user_context = user_contexts[from_whatsapp_number]
        if media_url:
            logger.info(f'Media received: {media_url} ({media_content_type})')
            auth = (account_sid, auth_token)
            image_response = requests.get(media_url, stream=True, auth=auth)
            if image_response.status_code == 200:
                unique_filename = generate_unique_filename('doc', 'jpg')
                user_folder = os.path.join(folder_path, from_whatsapp_number.replace(':', '_').replace('+', ''))
                os.makedirs(user_folder, exist_ok=True)
                image_path = os.path.join(user_folder, unique_filename)
                with open(image_path, 'wb') as img_file:
                    shutil.copyfileobj(image_response.raw, img_file)
                logger.info(f'Image successfully saved at {image_path}')
                if user_context['mode'] == 'awb':
                    results, color = process_image_and_generate_json(image_path, from_whatsapp_number, user_context)
                    logger.info(f'AWB processing results: {results}')
                    if color == 'green':
                        user_context['awb_processed'] = True
                    try:
                        output_json_path = user_context.get('current_json_path')
                        if not output_json_path or not os.path.exists(output_json_path):
                            raise FileNotFoundError(f'JSON file not found: {output_json_path}')
                        with open(output_json_path, 'r') as json_file:
                            processed_data = json.load(json_file)
                    except FileNotFoundError as e:
                        logger.error(f'Error reopening JSON file: {e}')
                        twilio_client.messages.create(from_=twilio_whatsapp_number, to=from_whatsapp_number, body='An error occurred while accessing the processed AWB data. Please try again.')
                        return ('Error', 500)
                    exporting_country = processed_data.get('exporting_country', 'Unknown').upper()
                    importing_country = processed_data.get('importing_country', 'Unknown').upper()
                    items = processed_data.get('cargo', {}).get('description', '')
                    relevant_regulations = processed_data.get('relevant_regulations')
                    user_context['exporting_country'] = exporting_country
                    user_context['importing_country'] = importing_country
                    user_context['relevant_regulations'] = relevant_regulations
                    requirements_message = get_country_requirements_message(exporting_country, importing_country, country_requirements)
                    user_context['requirements_message'] = requirements_message
                    missing_required = processed_data.get('missing_required_keys', [])
                    missing_optional = processed_data.get('missing_optional_keys', [])
                    formatted_missing_required = '\n'.join([f'- {key}' for key in missing_required]) if missing_required else 'None'
                    formatted_missing_optional = '\n'.join([f'- {key}' for key in missing_optional]) if missing_optional else 'None'
                    user_context['formatted_missing_optional'] = formatted_missing_optional
                    embargo_results = check_embargo_and_proximity(exporting_country, importing_country, items, embargo_data)
                    if embargo_results['alerts']:
                        embargo_message = '⚠️ ALERT: Potential embargo or restricted items detected:\n' + '\n'.join(embargo_results['alerts'])
                        twilio_client.messages.create(from_=twilio_whatsapp_number, to=from_whatsapp_number, body=embargo_message)
                    response_message = f'✅ AWB processed successfully!\n\n✅ All necessary fields are filled.\n\n⚠️ Missing optional details, type optional to check' if color == 'green' else f'❌ AWB processing failed.\n\nMissing required fields:\n{formatted_missing_required}\n\n⚠️ Missing optional details, type optional to check'
                    twilio_client.messages.create(from_=twilio_whatsapp_number, to=from_whatsapp_number, body=response_message)
                    next_step_message = f"Would you like to see the requirements for shipping from {exporting_country} to {importing_country}? Reply 'yes' or 'no'."
                    next_step_template_sid = account_sid
                    twilio_client.messages.create(from_=twilio_whatsapp_number, to=from_whatsapp_number, content_sid=next_step_template_sid, content_variables=json.dumps({'1': exporting_country, '2': importing_country}))
                elif user_context['mode'] == 'documents':
                    requirements_list = user_context.get('requirements_message', '').split('\n')
                    document_type = analyze_document_type(image_path, requirements_list)
                    user_context['document_analysis'].append({'path': image_path, 'type': document_type})
                    next_step_message = f"Document identified as: {document_type}. Upload more or reply 'done' when finished."
                    twilio_client.messages.create(from_=twilio_whatsapp_number, to=from_whatsapp_number, body=next_step_message)
            else:
                logger.error(f'Failed to download image. Status Code: {image_response.status_code}')
                response_message = 'Failed to download the image. Please try again.'
                twilio_client.messages.create(from_=twilio_whatsapp_number, to=from_whatsapp_number, body=response_message)
        elif body == 'optional' and user_context['mode'] == 'awb':
            formatted_missing_optional = user_context.get('formatted_missing_optional', 'No optional details available.')
            optional_response = f'⚠️ Missing airway bill optional details:\n{formatted_missing_optional}'
            twilio_client.messages.create(from_=twilio_whatsapp_number, to=from_whatsapp_number, body=optional_response)
        elif body == 'yes' and user_context['mode'] == 'awb':
            requirements_message = user_context.get('requirements_message', 'No requirements data available.')
            relevant_regulations = user_context.get('relevant_regulations')
            try:
                prompt = f'You are an AI assistant. Provide a shipping condition guidance based on the following regulations and provide all points needed but in a short paragraph with essential requirements and regulations:\n\n{relevant_regulations}'
                messages = [{'role': 'system', 'content': prompt}]
                response = azure_client.chat.completions.create(model='gpt-4o', messages=messages, temperature=0.7)
                if response.choices and response.choices[0].message:
                    summarized_regulations = response.choices[0].message.content.strip()
                else:
                    summarized_regulations = 'Unable to summarize the regulations at this time.'
            except Exception as e:
                logger.error(f'Error summarizing regulations: {e}')
                summarized_regulations = 'An error occurred while summarizing the regulations. Please try again later.'
            combined_message = f'{requirements_message}\n\nAttention to the regulations:\n{summarized_regulations}'
            user_context['mode'] = 'documents'
            twilio_client.messages.create(from_=twilio_whatsapp_number, to=from_whatsapp_number, body=combined_message)
            user_context['mode'] = 'documents'
            twilio_client.messages.create(from_=twilio_whatsapp_number, to=from_whatsapp_number, body="Now, please upload the required documents 1-by-1. Reply 'done' when finished.")
        elif body == 'go to scanning' and user_context['mode'] == 'awb':
            user_context['mode'] = 'documents'
            twilio_client.messages.create(from_=twilio_whatsapp_number, to=from_whatsapp_number, body="Please upload the required documents 1-by-1. Reply 'done' when finished.")
        elif body == 'done' and user_context['mode'] == 'documents':
            if not user_context.get('document_analysis', []):
                response_message = "No valid documents uploaded yet. Please upload the required documents and reply 'done' once all are uploaded."
            else:
                requirements_message = user_context.get('requirements_message', '')
                required_docs = [req.strip() for req in requirements_message.split('\n') if req.strip() and (not req.startswith('Requirements for'))]
                uploaded_types = {doc['type'] for doc in user_context['document_analysis']}
                if user_context.get('awb_processed'):
                    uploaded_types.add('Airway Bill')
                satisfied_docs = list(set([doc for doc in required_docs if doc in uploaded_types]))
                missing_docs = [doc for doc in required_docs if doc not in satisfied_docs]
                results = []
                for doc in satisfied_docs:
                    results.append(f'✅ {doc}')
                for doc in missing_docs:
                    results.append(f'❌ {doc}')
                extra_docs = [os.path.basename(doc['path']) for doc in user_context['document_analysis'] if doc['type'] not in required_docs]
                results.append('\n⚠️ Extra documents uploaded:')
                results.append('\n'.join((f'- {doc}' for doc in extra_docs)) if extra_docs else 'None')
                response_message = '\n'.join(results)
                user_contexts[from_whatsapp_number] = {'mode': 'awb', 'messages': [], 'requirements_message': None, 'uploaded_docs': [], 'document_analysis': [], 'awb_processed': False}
            twilio_client.messages.create(from_=twilio_whatsapp_number, to=from_whatsapp_number, body=response_message)
        elif body == 'Thank you' and user_context['mode'] == 'awb':
            response_message = 'My pleasure! Let me know if you need any other assistance.'
            twilio_client.messages.create(from_=twilio_whatsapp_number, to=from_whatsapp_number, body=response_message)
        elif body:
            if 'start' in body or 'hello' in body or 'hi' in body:
                user_context['mode'] = 'awb'
                response_message = 'Welcome to the Cargo Shipping Validator! Please send an image of the Air Waybill (AWB) to begin validation.'
                twilio_client.messages.create(from_=twilio_whatsapp_number, to=from_whatsapp_number, body=response_message)
            else:
                user_context['messages'].append({'role': 'user', 'content': body})
                prompt = 'You are VALIDOC, a system that validates cargo shipping documents and guides the customer to start with taking a photo of the airway bill and responds accordingly with short responses.'
                messages = [{'role': 'system', 'content': prompt}] + user_context['messages']
                try:
                    response = azure_client.chat.completions.create(model='gpt-4o', messages=messages, temperature=0.7)
                    if response.choices and response.choices[0].message:
                        ai_response = response.choices[0].message.content.strip()
                        response_message = ai_response
                        user_context['messages'].append({'role': 'assistant', 'content': ai_response})
                    else:
                        response_message = "I'm sorry, I couldn't process your request. Please try again."
                    twilio_client.messages.create(from_=twilio_whatsapp_number, to=from_whatsapp_number, body=response_message)
                except Exception as e:
                    logger.error(f'Error during OpenAI API call: {e}')
                    response_message = 'An internal error occurred while processing your request. Please try again later.'
                    twilio_client.messages.create(from_=twilio_whatsapp_number, to=from_whatsapp_number, body=response_message)
        else:
            response_message = 'No valid message detected. Please send a text or an image.'
            twilio_client.messages.create(from_=twilio_whatsapp_number, to=from_whatsapp_number, body=response_message)
        return ('OK', 200)
    except Exception as e:
        logger.error(f'Error processing message: {e}')
        response_message = f'An error occurred: {str(e)}'
        twilio_client.messages.create(from_=twilio_whatsapp_number, to=from_whatsapp_number, body=response_message)
        return ('Error', 500)

