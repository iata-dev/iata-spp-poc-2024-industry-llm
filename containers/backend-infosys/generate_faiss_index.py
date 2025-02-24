from generate_chunks import get_chunks
from save_chunks import save_chunks, are_chunks_available, load_chunks
from generate_embeddings import generate_embeddings_for_multiple_chunks, generate_embedding_for_single_chunk
from save_embeddings import are_embeddings_available, save_embeddings, load_embeddings
from save_index import create_index, is_index_available, save_index, load_index, get_matching_indices
from prompt_resp_using_llm import get_answer
import json

chunk_size = 1000
chunk_overlap = 200
chunks_file_location = "data/chunks.txt"
embeddings_file_location = "data/embeddings.npy"
index_file_location = "data/faiss_index.bin"

def get_chunks_local(regulatory_file_path):

    ## ---------- Generating Chunks --------------------
    chunks = []
    if not are_chunks_available(chunks_file_location):
        chunks = get_chunks(regulatory_file_path, chunk_size, chunk_overlap)
        save_chunks(chunks, chunks_file_location)
        print("Chunks saved successfully to the file storage...!!!")
    else:
        chunks = load_chunks(chunks_file_location)
        print("Chunks already available, reusing it...!!!")

    print(f"Total Chunks available/generated : {len(chunks)}")

    return chunks

def get_embeddings_local(chunks):
    ## ---------- Generating Embeddings --------------------
    embeddings = []
    if not are_embeddings_available(file_path=embeddings_file_location):
        embeddings = generate_embeddings_for_multiple_chunks(chunks=chunks)
        save_embeddings(file_path=embeddings_file_location,embeddings=embeddings)
        print("Embeddings save successfully to the file storage...!!!")
    else:
        embeddings = load_embeddings(file_path=embeddings_file_location)
        print("Embeddings already available, reusing it...!!!")

    print(f"Total Embeddings available/generated : {len(embeddings)}")

    return embeddings

def get_faiss_index(embeddings):
    #--------------- Create FAISS Index ------------------------
    index = []
    if not is_index_available(file_path=index_file_location):
        index = create_index(embeddings=embeddings)
        save_index(file_path=index_file_location,index=index)
        print("FAISS Index saved successfully to the file storage...!!!")
    else:
        index = load_index(file_path=index_file_location)
        print("FAISS Index already available, reusing it...!!!")

    print(f"Number of Embeddings inside index : {index.ntotal}")

    return index

def generate_faiss_index(regulatory_file_path):

    chunks = get_chunks_local(regulatory_file_path)
    embeddings = get_embeddings_local(chunks)

    return get_faiss_index(embeddings), chunks

def validate_faiss_index_with_openai(index, chunks) :

    #------------------- Similarity Search for input query ----------------
    input_query = "What are the document to be produced for the perishable goods? Please provide the documents list in a comma seaprated list."
    input_query_embedding = generate_embedding_for_single_chunk(chunk=input_query)

    distances, indices = get_matching_indices(index=index, query_embedding=input_query_embedding)

    print( distances, indices)

    context = []
    for index in indices[0] :
        context.append(chunks[index])

    #--------------------------- Get Answers from OpenAI API --------------------------------
    answer = get_answer(input_query=input_query, context_messages=context)

    json_object = json.loads(answer)

    print(f"Response from OpenAI : {json_object["choices"][0]["message"]["content"]}")

if __name__ == "__main__":

    regulatory_doc_location = r"data/RegulatoryDocument.docx"

    index, chunks = generate_faiss_index(regulatory_doc_location)

    #validate_faiss_index_with_openai(index, chunks)

    