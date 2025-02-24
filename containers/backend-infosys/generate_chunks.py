from docx import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_word_document(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def get_chunks(file_path, chunk_size, chunk_overlap):    
    document_text = load_word_document(file_path)  
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_text(document_text)
    return chunks