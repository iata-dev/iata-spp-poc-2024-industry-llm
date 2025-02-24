import tiktoken

def calculate_token_count(prompt, base64_image):
    """Calculate the token count for the prompt and image base64 data."""
    encoding = tiktoken.encoding_for_model('gpt-4')
    full_message = f'{prompt}\nImage (base64): {base64_image}'
    total_tokens = len(encoding.encode(full_message))
    return total_tokens

