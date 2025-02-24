# SITA Cargo Shipping Validator

This project is a cargo shipping validation system using Twilio's WhatsApp API and Multimodal LLM for document processing and regulatory compliance validation (also included a WebUI frontend version).

![GIF Description](/assets/SITA.gif)

## SITA Solution - technical details
This Python application facilitates image analysis using Azure OpenAI’s GPT-4o model by encoding images into base64 format and integrating them into structured prompts. The encode_image function reads an image file, converts it to base64 encoding, and returns it as a string while handling exceptions. The calculate_token_count function determines the number of tokens used by the prompt and the base64-encoded image, ensuring compliance with GPT-4o’s token limits. The analyze_image function constructs an OpenAI API request by embedding the encoded image alongside a custom text prompt within a structured message format, sending the request to Azure OpenAI, and returning the model’s response while handling errors.

This application processes regulatory documents, extracts relevant values, and creates a vector store for retrieval. The extract_value function searches a given text for a specific key-value pair formatted in JSON-like syntax using regex, returning the extracted value or an empty string if not found. The load_document function scans a specified folder for supported document formats (.pdf, .txt, .docx), loads their content using appropriate methods (e.g., UnstructuredWordDocumentLoader for Word files and plain file reading for text files), and prepares them for further processing. Placeholder logic is included for PDF handling. Once loaded, the text is split into manageable chunks using CharacterTextSplitter to ensure efficient retrieval. The create_vector_store function then generates embeddings using OpenAI’s embedding model and stores them in a FAISS-based vector database, enabling semantic search and retrieval of relevant document segments.

This application processes an Air Waybill (AWB) image, extracts structured data, validates required fields, and retrieves relevant regulatory information. The process_image_and_generate_json function first analyzes the AWB image using analyze_image, passing a structured JSON extraction prompt to Azure OpenAI. Extracted values are dynamically retrieved using extract_value and organized into a structured JSON format. The script then integrates a Retrieval-Augmented Generation (RAG) system by loading regulatory documents, converting them into vector embeddings with FAISS, and querying relevant sections based on the cargo description. Validation checks identify missing required or optional fields, and results are saved as a uniquely named JSON file while updating the user’s context. The function returns validation feedback with color-coded messages indicating whether required information is complete or missing.

This application facilitates document validation, embargo checks, and country-specific export/import compliance for air cargo shipments. The get_country_requirements_message function retrieves export and import requirements from a JSON dataset based on Alpha-2 country codes, formatting them into a readable message. The get_embargo_info function checks if an importing country is under trade restrictions, while check_embargo_and_proximity extends this by verifying embargoed items and assessing proximity risks using Azure OpenAI. The script loads JSON files containing regulatory and embargo data, ensuring they are correctly parsed. The analyze_document_type function employs Azure OpenAI to classify uploaded documents against predefined shipping requirements. The validate_document_details function identifies missing mandatory and optional fields in extracted shipping data, while validate_uploaded_documents compares uploaded files against required document lists, marking missing and extra documents accordingly. These processes are integrated into a Flask-based web application, using a global dictionary to manage user-specific chat contexts for seamless interaction.

This Flask-based WhatsApp webhook processes cargo shipping documents using Twilio, Azure OpenAI, and regulatory data validation. When a user sends an image, the script extracts their WhatsApp number and processes the media, saving it locally. If the image is an Air Waybill (AWB), it triggers process_image_and_generate_json, extracting structured shipment details, validating missing fields, and checking for embargoes and proximity risks. If successful, it retrieves relevant shipping regulations and presents users with export/import requirements. Users can upload additional documents, which are analyzed with analyze_document_type and validated against regulatory requirements. The system dynamically tracks user context, managing different workflow states such as AWB processing, document collection, and regulatory compliance checks. Users can inquire about missing details, request regulatory summaries, or proceed to scanning. The webhook also processes free-text queries using Azure OpenAI, ensuring guided and efficient document validation for cargo shipments.

## Prerequisites Prerequisites

- **Python 3.6 or newer**: Ensure Python is installed on your system. [Download Python](https://www.python.org/)
- **Twilio Account**: Sign up for a Twilio account. You will need your **Twilio Account SID** and **Auth Token**.
- **WhatsApp Account**: You need an active WhatsApp account for testing.
- **Azure OpenAI or OpenAI Account**: Ensure you have API access to Azure OpenAI.

## Setup Twilio's WhatsApp Sandbox

1. Log in to the **Twilio Console** and navigate to **Messaging > Try it Out > Send a WhatsApp Message**.
2. Follow the instructions to send the provided **join code** to Twilio's sandbox number.

## Set Up the Development Environment

### 1. Create a Project Directory and Virtual Environment
```sh
mkdir whatsapp-flask-app
cd whatsapp-flask-app
python3 -m venv venv
source venv/bin/activate  # For Unix/macOS
venv\Scripts\activate  # For Windows
```

### 2. Install Required Packages
```sh
pip install flask twilio python-dotenv pdf2image pillow openai langchain-openai langchain requests psutil signal
```

### 3. Configure Environment Variables
Create a `.env` file and add:
```sh
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=your_twilio_whatsapp_number
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_OPENAI_API_KEY=your_azure_api_key
AZURE_OPENAI_DEPLOYMENT=your_azure_deployment
AZURE_OPENAI_VERSION=your_azure_version
```

## Running the Application

### 1. Start the Flask Server
```sh
python main.py
```
The server runs on port **5001** by default.

### 2. Expose the Local Server (for example using ngrok)
If testing locally, install and run `ngrok` to expose your Flask server:
```sh
ngrok http 5001
```
Copy the `https://<your-ngrok-url>.ngrok.io` and set it as the **Webhook URL** in Twilio Console.

## Features

### 1. Receive and Process Air Waybill (AWB) Documents
- Users send AWB images via WhatsApp.
- The system extracts information using Azure OpenAI.
- It checks for missing details and regulatory compliance.

### 2. Validate Shipping Documents
- Extract document information from images.
- Check compliance with import/export regulations.
- Identify missing required and optional details.

### 3. Embargo and Proximity Checks
- Validates if shipments are restricted due to embargoes.
- Assesses risks based on proximity to restricted countries.

### 4. Automated WhatsApp Responses
- Dynamically guides users through document validation.
- Sends missing document alerts and next steps.

## API Endpoints

### 1. WhatsApp Webhook
`POST /whatsapp`
- Handles incoming WhatsApp messages.
- Processes AWB and document images.
- Responds dynamically based on user interactions.

### 2. Home Route
`GET /`
- Runs document processing and validation if in debug mode.

## Deployment
For production deployment:
- Use `gunicorn` for better performance.
- Deploy on a cloud service (AWS, Azure, Google Cloud) with a public domain.

## Contact
**Developed by Sid Ryan**  
Email: [sid.ryan@sita.aero](mailto:sid.ryan@sita.aero)
