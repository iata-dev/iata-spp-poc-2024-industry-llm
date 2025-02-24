import openai
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Set your API key and endpoint
openai.api_key = config['DEFAULT']['openai.api_key']
openai.api_base = config['DEFAULT']['openai.api_url']
openai.api_type = config['DEFAULT']['openai.api_type']
openai.api_version = config['DEFAULT']['openai.api_version']
deployment_name = config['DEFAULT']['embedding.model_name']

# Function to generate an embedding for a given text using the new API
def generate_embedding_for_single_chunk(chunk):

    response = openai.Embedding.create(
        input=chunk, 
        engine=deployment_name, 
    )

    print("Embedding generated using azure openai API...!!!")

    return response['data'][0]['embedding']

def generate_embeddings_for_multiple_chunks(chunks):

    embeddings = []
    counter = 1
    for chunk in chunks:
        embedding = generate_embedding_for_single_chunk(chunk)
        embeddings.append(embedding)
        print(f"Embedding : {counter}")
        counter += 1

    return embeddings
    

if __name__ == "__main__":
    text1 = "This is a simple example text1."
    text2 = "This is a simple example text2."

    chunks = [text1, text2]
    embeddings = generate_embeddings_for_multiple_chunks(chunks)
    for embedding in embeddings:
        print(embedding)