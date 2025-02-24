# Infosys Backend with Azure Resources and Docker

This guide provides instructions to set up and run infosys backend application using Azure resources and Docker.

## Prerequisites

- Azure account
- Docker installed on your machine

## Azure Resources

### 1. Create Azure Resources

#### OpenAI API
- Create Azure OpenAI Resource by selecting the required fields including Subscription, Resourece group, Region, Pricing Tier etc.
  - <img width="705" alt="OpenAI1" src="https://github.com/user-attachments/assets/331ec229-7103-4165-87c2-04fb6acf51ff" />
- Select the created OpenAI resource and get the Key and endpoint details. Please find the below screenshot for reference.
  <img width="762" alt="OpenAI2" src="https://github.com/user-attachments/assets/155eb56c-a2d4-4655-b9b9-96f20bcb788b" />
- Goto overview section and click on Explore Azure AI Foundry portal to create the required deployment models
  - **Embedding Model**
  - **LLM Model**
    <img width="803" alt="OpenAI3" src="https://github.com/user-attachments/assets/4053cf64-b395-40c1-8846-ed8ccc24755b" />

- Inside the Azure AI Foundry portal, create the deployment model 'text-embedding-ada-002' and 'gpt-4o'. please refer to the following screenshots for reference.
  <img width="726" alt="OpenAI4" src="https://github.com/user-attachments/assets/25551402-dd86-45ee-a9c6-a92d223e7dff" />
  <img width="888" alt="OpenAI5" src="https://github.com/user-attachments/assets/3ea32364-a2ac-4785-9b63-37aa60ba6e66" />
  <img width="888" alt="OpenAI6" src="https://github.com/user-attachments/assets/6599e99c-8045-4ade-b277-531b70f2f732" />







#### Document Intelligence
- Create Azure Document Intelligence(DI) Resource by selecting the required fields including Subscription, Resourece group, Region, Pricing Tier etc.
  <img width="725" alt="DI1" src="https://github.com/user-attachments/assets/0c45c9f3-dd62-4f85-8f20-b85324aadb56" />
- Select the created DI resource and get the Key and endpoint details. Please find the below screenshot for reference.
  <img width="796" alt="DI2" src="https://github.com/user-attachments/assets/ca290a6c-58bf-4cd8-a5fc-56e5101460cd" />



### 2. Update `config.ini` File

Update the `config.ini` file with the following information:

- **API Key**: Your API key for the OpenAI API
- **URL**: The URL for the OpenAI API
- **API Type**: The type of API (e.g., `openai`)
- **API Version**: The version of the API
- **Embeddings Model Name**: The name of the embeddings model (text-embedding-ada-002)
- **LLM Model Name**: The name of the LLM model (GPT-4 used and tested)
- **API Key for Azure Document Intelligence**: Your API key for Azure Document Intelligence
- **API URL for Azure Document Intelligence**: The URL for Azure Document Intelligence



### 3. Build the Docker image:
    docker build -t iata-infosys-backend .

### 4. Build the Docker image:
    docker run -p 5000:5000 iata-infosys-backend

 ### 5. Test API(s):
    
- Postman collection "Validate IATA APIs.postman_collection" has been added to the repository. It consists of couple of requests to cover both happy path and negative scenarios.
- Import this collection to the Postman, make changes to the input as requied to test the APIs.
    

### 5. Generate FAISS Index:

- Place regulatory document inside the `/uploads` folder with the name `RegulatoryDocument.docx`
- Run the Python file `generate_faiss_index.py` using the command `python .\generate_faiss_index.py`

### 6. Execute Test Cases:

- Postman collection has been uploaded with name `/test_cases/Test Cases.postman_collection`. This Postman collection consists several test cases
- Import this postman collection and execute each test case to validate result




### TODO: Add code for accuracy matrices



Detiled Documenation and future enhancements:

Perishable Cargo Document Processing System Technical Documentation
1. System Overview
A Perishable cargo document validation system that combines vector similarity search (FAISS) where PCR document embeddings are stored, Azure OpenAI's GPT-4 (with Appropriate Prompts), and Azure Document Intelligence for processing and validating shipping documents. Overall API orchestrated in managed through Python flask framework.

API 1 : /upload64 (accepts base64 Airway Bill and validates and responds with JSON)
API2 : /requireddocs (accepts information from AWB like source , destination and type of Perishable goods and returns all required document list)
API3: / validatedocs (accepts base 64 , AWB , Phytosanitary , Invoice and validate the contain against each other and also validates against the PCR document)

![image](https://github.com/user-attachments/assets/73a38727-5f3d-4932-87b0-a99adbc65a70)

 
2. Core Components
2.1 Document Intelligence Module (read_doc_using_di.py)
●	Purpose: Extracts text content from documents using Azure Document Intelligence
●	Key Functions:
○	extract_doc(path): Main document processing function
○	get_content_using_di(file_path): Simplified text extraction interface
●	Dependencies: Azure Document Intelligence SDK
2.2 LLM Processing Module (prompt_resp_using_llm.py)
●	Purpose: Handles vector search and LLM interactions
●	Key Functions:
○	get_answer(input_query, context_messages): LLM interaction handler
○	are_documents_uploaded_valid(uploadedDocuments): Document validation
○	is_goods_perishable(natureOfGoods): Goods classification
●	Dependencies:
○	FAISS vector database
○	Azure OpenAI
○	Custom embedding generation
○	Prompt Engineering
3. System Architecture
3.1 Data Flow
1.	Document Ingestion
○	Input: PDF/Image documents
○	Process: OCR via Azure Document Intelligence
○	Output: Extracted JSON content
2.	Vector Processing
○	Input: Extracted text
○	Process: Embedding generation
○	Storage: FAISS index
3.	Document Validation1 - Provides list of required documents 
○	Input: User query/documents , Various Prompts
○	Process: Vector similarity search + LLM processing
○	Output: Validation results - list of mandatory document for source and destination
4.	Document Validation2 - Comparison of documents to ensure they are co-related and key information present as per PCR guidelines 
○	Input: User query/documents , Various Prompts
○	Process: Vector similarity search + LLM processing
○	Output: Validation results - documents matches , and as per PCR guidelines
3.2 Storage Components
●	FAISS Index: data/faiss_index.bin
●	Document Chunks: data/chunks.txt
4. Configuration Requirements
4.1 Azure Services
Config.ini

4.2 System Requirements
●	Python 3.12+
●	FAISS library
●	Azure SDK packages
●	Sufficient storage for vector indices
●	Azure Document Intelligence resources
●	Azure Open AI with Azure AI Foundry 
5. Error Handling
5.1 Document Processing Errors
●	Invalid file formats
●	OCR processing failures
●	Network connectivity issues
5.2 Vector Search Errors
●	Index loading failures
●	Embedding generation errors
●	Similarity search failures
5.3 LLM Processing Errors
●	API rate limits
●	Context length exceeded
●	Invalid responses

Additional Enhancement in future for Production grade application  

6. Security Considerations
6.1 API Security
●	Secure credential storage
●	API key rotation
●	Request/Response encryption
6.2 Data Security
●	In-memory processing
●	No persistent document storage
●	Access control implementation
7. Performance Optimization
7.1 Document Processing
●	Batch processing implementation
●	Caching mechanisms
●	Resource cleanup
7.2 Vector Search
●	Index optimization for large PCR documents
●	Query performance tuning
●	Result caching
8. Monitoring and Logging
8.1 Key Metrics
●	Document processing time
●	API response times
●	Error rates
●	Resource usage
8.2 Logging Requirements
●	Processing events
●	Error tracking
●	Performance metrics
●	Usage statistics
9. Maintenance Procedures
9.1 Regular Tasks
●	Index optimization
●	Cache clearing
●	Log rotation
●	API key rotation
9.2 Troubleshooting
●	Error log analysis
●	Performance monitoring
●	System health checks
10. Additional Enhancements
●	Batch processing support
●	Custom document models for other type of Cargo documents
●	Async processing (as large number of document validation would take time)
●	Webhook integration
●	Enhanced error reporting
●	Result caching
●	LLM and RAG Metrix to validate the accuracy of result



