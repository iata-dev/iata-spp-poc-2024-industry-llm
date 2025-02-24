def analyze_image(image_path, custom_prompt):
    """Analyze an image using Azure OpenAI with the client object."""
    try:
        base64_image = encode_image(image_path)
        messages = [{'role': 'system', 'content': 'You are an AI assistant.'}, {'role': 'user', 'content': [{'type': 'text', 'text': custom_prompt}, {'type': 'image_url', 'image_url': {'url': f'data:image/jpeg;base64,{base64_image}'}}]}]
        response = azure_client.chat.completions.create(model='gpt-4o', messages=messages, temperature=0.7)
        if isinstance(response, dict) and 'choices' in response:
            return response['choices'][0]['message']['content']
        else:
            return f'Unexpected API response format: {response}'
    except Exception as e:
        return f'Error analyzing image {image_path}: {e}'
