VALIDOC Architecture

Overview

VALIDOC is an AI-driven document validation system that integrates WhatsApp via Twilio, utilizes Retrieval-Augmented Generation (RAG) for regulation compliance, and ensures seamless cargo shipping operations by validating documents, checking embargo restrictions, and enforcing shipping regulations.

System Architecture

VALIDOC consists of multiple interconnected components, each responsible for specific tasks within the validation process.

1. User Interaction Layer

WhatsApp Interface (Twilio API):

Captures user messages and uploaded document images.

Sends validation results and compliance updates to the user.

Flask API Server:

Handles incoming requests from Twilio’s webhook.

Processes document validation logic.

Responds to user queries.

2. Processing Layer

Document Parsing & Extraction:

Uses PDF2Image & Pillow to process and extract data from images.

OCR-based text extraction (if needed for further enhancement).

Validation & Compliance Checks:

Checks document completeness.

Cross-references extracted data against shipping regulations.

Retrieves missing or incorrect data fields.

Regulatory Compliance (RAG):

Fetches country-specific trade regulations from an external database.

Analyzes shipping documentation requirements.

Identifies missing permits or documentation.

Embargo & Restricted Items Check:

Uses embargo databases to verify if the destination country has active restrictions.

Flags prohibited goods and materials.

3. AI & Knowledge Retrieval Layer

Azure OpenAI for RAG:

Retrieves the latest shipping rules and regulations.

Generates compliance summaries for user guidance.

Improves accuracy by incorporating real-time policy updates.

FAISS Vector Store:

Stores and retrieves regulation documents for fast access.

Enables similarity search for regulations related to specific goods or countries.

4. Storage & Database Layer

Local Storage & Logs:

Saves processed AWB images and extracted data.

Maintains a log of user interactions for auditing.

Regulatory Data Sources:

Structured JSON files storing:

Country-specific import/export regulations.

Embargoed country lists.

Perishable cargo handling guidelines.

5. Deployment & Scalability

Flask API Hosted on Cloud or Local Server

Supports horizontal scaling using Gunicorn & Nginx.

Can be containerized using Docker.

Webhook Exposure using ngrok (for development/testing)

Allows secure tunneling to the local development environment.

Workflow Diagram

User uploads AWB via WhatsApp → Twilio forwards to Flask API

Flask API processes AWB → Extracts key data → Stores missing fields

RAG fetches country-specific regulations → Flags required documents

Embargo system verifies country restrictions → Alerts if embargoed

Validation results are compiled → Response sent to user via WhatsApp

Key Benefits of the Architecture

Automated Compliance Validation: Ensures all required documents are present before shipping.

Scalable & Modular: Each component can be independently extended or replaced.

Real-time Updates: RAG integration ensures regulations are always up to date.

Secure & Reliable: Data encryption and logs maintain compliance and traceability.

Contact

For support, contact Sid Ryan at sid.ryan@sita.aero.
