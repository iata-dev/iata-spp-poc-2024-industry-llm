def load_document(folder_path):
    supported_extensions = ('.pdf', '.txt', '.docx')
    all_documents = []
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(supported_extensions):
            file_path = os.path.join(folder_path, file_name)
            try:
                if file_name.lower().endswith('.docx'):
                    loader = UnstructuredWordDocumentLoader(file_path)
                    documents = loader.load()
                elif file_name.lower().endswith('.txt'):
                    with open(file_path, 'r', encoding='utf-8') as file:
                        text = file.read()
                        documents = [{'content': text}]
                elif file_name.lower().endswith('.pdf'):
                    documents = [{'content': f'PDF content from {file_name} (processing to be added)'}]
                all_documents.extend(documents)
            except Exception as e:
                logger.error(f'Error processing file {file_path}: {e}')
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_documents = text_splitter.split_documents(all_documents)
    return split_documents
