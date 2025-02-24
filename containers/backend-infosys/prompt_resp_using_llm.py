import openai
import json
from generate_embeddings import generate_embedding_for_single_chunk
from save_index import get_matching_indices, load_index, is_index_available
from save_chunks import load_chunks
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Set your API key and endpoint
openai.api_key = config['DEFAULT']['openai.api_key']
openai.api_base = config['DEFAULT']['openai.api_url']
openai.api_type = config['DEFAULT']['openai.api_type']
openai.api_version = config['DEFAULT']['openai.api_version']
deployment_name = config['DEFAULT']['llm.model_name']

chunks_file_location = "data/chunks.txt"
index_file_location = "data/faiss_index.bin"

prompt_is_perishable_goods = """From the context, it consists of couple of goods that are being 
                            shipped from one destination to another. Please find the goods in it 
                            and provide me strictly a one word answer whether the goods mentioned 
                            in the context is perishable or not? Provide me Yes or No answer only."""


# Function to generate an embedding for a given text using the new API
def get_answer(input_query, context_messages):

    messages = prepare_messages_object(input_query=input_query, context_messages=context_messages)

    response = openai.ChatCompletion.create(
        deployment_id=deployment_name,
        messages=messages,
        max_tokens=500,
        temperature=0.0
    )

    return json.dumps(response, indent=4)

def prepare_messages_object(input_query, context_messages) :

    message = []
    message.append({"role":"system", "content": "You are a helpful assistant"})
    message.append({"role":"user", "content": input_query})
    for context in context_messages:
        message.append({"role":"system", "content": context})
    
    return message

def get_answer_from_answer_object(answerObject) :
    answer_dict = json.loads(answerObject)
    answer = answer_dict["choices"][0]["message"]["content"]
    return answer

def is_goods_perishable(natureOfGoods) :
    answerObject = get_answer(input_query=prompt_is_perishable_goods, context_messages=[natureOfGoods])
    return get_answer_from_answer_object(answerObject)

def are_documents_uploaded_valid(uploadedDocuments, mandatoryDocs) :
    #------------------- Similarity Search for input prompt ----------------
    if uploadedDocuments.strip() :

        prompt_validate_documents = f"""As per the requirement the minimum set of documents that are
                            required for perishable goods are {mandatoryDocs}.
                            Please provide me Yes or No along with reasoning,
                            if the input documents provided are meeting the minimum document 
                            requirements. Please skip CITES related document requirements.
                            The documents end user has provided are : {uploadedDocuments} """
        
        context_messages = []

        if is_index_available(index_file_location) :
            input_query_embedding = generate_embedding_for_single_chunk(chunk=prompt_validate_documents)
            index = load_index(file_path=index_file_location)
            distances, indices = get_matching_indices(index=index, query_embedding=input_query_embedding)
            chunks = load_chunks(chunks_file_location)  
        
            
            for index in indices[0] :
                context_messages.append(chunks[index])
        
        #--------------------------- Get Answers from OpenAI API --------------------------------
        answerObject = get_answer(input_query=prompt_validate_documents, context_messages=context_messages)

        return get_answer_from_answer_object(answerObject)
    else: 
        return "No."
    
if __name__ == "__main__":
    uploadedDocuments = "Air WayBill, Phytosanitory, Other"
    answer = are_documents_uploaded_valid(uploadedDocuments)
    print("Answer: ", answer)