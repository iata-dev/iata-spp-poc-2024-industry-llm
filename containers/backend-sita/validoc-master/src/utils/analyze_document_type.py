def analyze_document_type(image_path, requirements_list):
    """
    Analyze the uploaded document and match it with the requirements list.
    """
    try:
        base64_image = encode_image(image_path)
        custom_prompt = f"Analyze the uploaded image and identify the document type. Match it to one of the following requirements: {', '.join(requirements_list)}. Respond in the exact format: 'Document Type: <document_type>'. If the type is not in the list, respond with 'Document Type: Unknown'."
        messages = [{'role': 'system', 'content': 'You are a document analyzer for cargo shipping.'}, {'role': 'user', 'content': [{'type': 'text', 'text': custom_prompt}, {'type': 'image_url', 'image_url': {'url': f'data:image/jpeg;base64,{base64_image}'}}]}]
        response = azure_client.chat.completions.create(model='gpt-4o', messages=messages, temperature=0.7)
        print(response)
        content = response.choices[0].message.content.strip()
        logger.info(f'API Response: {content}')
        if content.startswith('Document Type:'):
            document_type = content.split('Document Type:')[1].strip()
            return document_type
        else:
            logger.error(f'Unexpected API response format: {content}')
            return 'Unknown'
    except Exception as e:
        logger.error(f'Error analyzing document type: {e}')
        return 'Unknown'
