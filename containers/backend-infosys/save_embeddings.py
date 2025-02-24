import numpy as np
import os

def are_embeddings_available(file_path):
    return  os.path.exists(file_path) and os.path.getsize(file_path) > 0 

def save_embeddings(file_path,embeddings):
    np.save(file_path, embeddings)

def load_embeddings(file_path):
    return np.load(file_path)

if __name__ == "__main__":    
    embedding1 = np.array([0.1, 0.2, 0.3, 0.4])
    embedding2 = np.array([0.5, 0.6, 0.7, 0.8])
    embedding3 = np.array([0.9, 1.0, 1.1, 1.2])

    # Combine embeddings into a single numpy array
    embeddings = np.array([embedding1, embedding2, embedding3])
    file_name = 'data/embedding.npy'
    save_embeddings(embeddings=embeddings, file_path=file_name)
    print(f"Data has been successfully saved to {file_name}.")
    loaded_embeddings = load_embeddings(file_name)
    print(f" Loaded embeddings : {loaded_embeddings}.")