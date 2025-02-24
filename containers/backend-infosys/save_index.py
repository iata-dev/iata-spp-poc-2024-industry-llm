import faiss
import numpy as np
import os

nearest_neighbors = 7

def is_index_available(file_path):
    return  os.path.exists(file_path) and os.path.getsize(file_path) > 0 

def create_index(embeddings) :
    # Convert embeddings to float32
    embeddings = np.array(embeddings).astype('float32')
    # Create a FAISS index
    dimension = embeddings.shape[1]
    print (f"Dimension:{dimension}")
    index = faiss.IndexFlatL2(dimension)  # L2 distance
    # Add embeddings to the index
    index.add(embeddings)
    print(f"Index : {index}")
    return index

def save_index(file_path, index) :
    faiss.write_index(index, file_path)

def load_index(file_path) :
    return faiss.read_index(file_path)

def get_matching_indices(index, query_embedding) :

    input_embedding = np.array(query_embedding).astype('float32')

    # Ensure the query embedding is 2D
    if input_embedding.ndim == 1:
        input_embedding = input_embedding.reshape(1, -1)
   
    distances, indices = index.search(input_embedding, nearest_neighbors)

    return distances, indices
