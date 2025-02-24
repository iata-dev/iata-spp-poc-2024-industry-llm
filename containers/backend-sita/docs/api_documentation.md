# API Setup for VALIDOC

## Overview
VALIDOC is a Multimodal LLM document validation system integrated with WhatsApp using Twilio. It processes Air Waybills (AWB), verifies shipping documents, checks embargo restrictions, and ensures regulatory compliance using **Retrieval-Augmented Generation (RAG)**.

## Prerequisites
- **Python 3.6 or newer**
- **Flask Framework**
- **Twilio API for WhatsApp Messaging**
- **Azure OpenAI API for RAG and AI Processing**
- **ngrok for local webhook testing**

---
## Installation
### 1. Clone the Repository
```sh
git clone https://github.com/your-repo/validoc.git
cd validoc
```

### 2. Create a Virtual Environment
```sh
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project directory and add:
```sh
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=your_twilio_whatsapp_number
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_OPENAI_API_KEY=your_azure_api_key
AZURE_OPENAI_DEPLOYMENT=your_azure_deployment
AZURE_OPENAI_VERSION=your_azure_version
```

---
## Running the API
### 1. Start the Flask Server
```sh
python app.py
```
- The server runs on `http://127.0.0.1:5001` by default.

### 2. Expose the Server using ngrok
```sh
ngrok http 5001
```
- Copy the generated `https://your-ngrok-url.ngrok.io`.
- Set it as the **Webhook URL** in your Twilio Console.

---
## API Endpoints

### **1. WhatsApp Webhook**
```
POST /whatsapp
```
Handles incoming WhatsApp messages, AWB processing, and document validation.

**Request Example:**
```json
{
  "From": "whatsapp:+1234567890",
  "Body": "Validate AWB",
  "MediaUrl0": "https://image-url.com/awb.jpg"
}
```

**Response Example:**
```json
{
  "status": "AWB processed successfully",
  "awb_number": "123-45678910",
  "missing_fields": []
}
```

---
### **2. Validate Documents**
```
POST /validate-documents
```
Checks if uploaded documents meet shipping regulations.

**Request Example:**
```json
{
  "documents": [
    { "type": "Packing List", "file": "base64_encoded_string" },
    { "type": "Certificate of Origin", "file": "base64_encoded_string" }
  ]
}
```

**Response Example:**
```json
{
  "valid": true,
  "missing_documents": [],
  "warnings": []
}
```

---
### **3. Fetch Country Regulations**
```
GET /regulations/{country_code}
```
Retrieves the latest shipping regulations for a given country.

**Response Example:**
```json
{
  "country": "XX",
  "export_requirements": ["Airway Bill", "Commercial Invoice"],
  "import_requirements": ["Import Permit", "Customs Declaration"],
  "special_conditions": "Additional clearance required for hazardous materials."
}
```

---
### **4. Check Embargo Status**
```
GET /embargo/{country_code}
```
Checks if a country has active trade embargoes.

**Response Example:**
```json
{
  "country": "XX",
  "embargoed": true,
  "restricted_items": ["Military-grade equipment", "Advanced encryption software"]
}
```

---
## Deployment
- **Production Deployment:** Use Gunicorn and Nginx for better performance.
- **Cloud Hosting:** Deploy on AWS, Azure, or Google Cloud for scalability.

```sh
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

---
## Contact
For support, contact **Sid Ryan** at `sid.ryan@sita.aero`.
