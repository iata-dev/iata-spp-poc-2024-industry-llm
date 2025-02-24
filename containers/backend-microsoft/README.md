# MICROSOFT POC OVERVIEW

This project contains both the backend (`validation_backend.py`) and the frontend (`streamlit_validation_interface.py`) for validation of the documents required for perishable air cargo import/export, as per requirements from IATA and their air carrier business partners (LATAM, ALL NIPPON AIRWAYS, QATAR AIRWAYS).

# INSTALL INSTRUCTIONS 

## PREPARE THE RUNTIME

1. install the requirements using:

> pip install -r requirements.txt

2. Poppler is used by the `pdf2image` library. This POC comes with a versoin of POPPLER pre-compiled for Windows and the `convert_from_bytes()` function referencing the location as a relative path. It's possible that the runtime you are targeting needs a different compilation of POPPLER, in that case, you'll need to compile it, add it to the ENV variable PATH and refer the `convert_from_bytes()` function to it.

## PREPARE THE AZURE RESOURCES

### DEPLOYING AI FOUNDRY AND PROVISIONING OPENAI MODEL

1. Create an [Azure AI Foundry Hub](https://learn.microsoft.com/en-us/azure/ai-studio/how-to/create-azure-ai-resource?tabs=portal) resource on your Azure tenant (or use existing one if you have it already). If you are starting from scratch, you need to create a new Azure OpenAI resource, which will be automatically connected to the hub ("Azure AI services base models -- Connect AI Services incl. OpenAI" -> "Create New")
2. [Deploy a new OpenAI GPT4o model](https://learn.microsoft.com/en-us/azure/ai-foundry/model-inference/how-to/create-model-deployments?pivots=ai-foundry-portal#add-a-model) in AI Foundry Hub's project from the "Model Catalog" section. Get the key and endpoint (Target URI) of your deployed model from the "Models + endpoints" section. (Target URI typically looks like: https://<your-resource-name>.openai.azure.com/gpt-4o/chat/completions?api-version=2024-08-01-preview)
3. Update the ".env" file, filling out the AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT variables with the values you got from step #2

### DEPLOYING DOCUMENT INTELLIGENCE INSTANCE

1. Create a [Document Intelligence](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/how-to-guides/create-document-intelligence-resource?view=doc-intel-4.0.0#create-a-resource) resource on your Azure tenant (or use existing one if you have it already).
2. Get [API Key and Endpoint URL](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/how-to-guides/create-document-intelligence-resource?view=doc-intel-4.0.0#get-endpoint-url-and-keys) from you Document Intelligence resource.
3. Update the `.env` file, filling out the DOCUMENTINTELLIGENCE_API_KEY and DOCUMENTINTELLIGENCE_ENDPOINT variables with the values you got from step #2

## LAUNCH THE VALIDATOR

1. Launch the Streamlit by running the command:

> streamlit run path\to\repo\iata-spp-poc-2024-industry-llm\containers\microsoft\streamlit_validation_interface.py

Alternatively, you can launch using the command: 

> python -m streamlit run path\to\repo\iata-spp-poc-2024-industry-llm\containers\microsoft\streamlit_validation_interface.py

### BATCH VALIDATION mode

Follow these steps, if you need to validate multiple cases in succession.

1. Extract IATA POC validation files to a location of your choice (each validation case has own folder, such as 'ANBKF1', 'ANBKF2', 'LABMF1', etc )
2. Update the `validation_path` variable in `batch_validation_mode.py` with the path to the extracted files
3. Run `batch_validation_mode.py`
4. For each validation case a JSON with validation response will be created in each validation case folder 


# INSTRUCTIONS (USER GUIDE)
1. Upload a set of airway bill documents in PDF format. You can upload multiple files and each file can contain multiple documents related to the airway bill.

2. Click the 'Validate Documents' button to start the validation process. The validation process will classify the documents, extract information and validate the documents against a set of validation rules that are dynamically determined as appropriate based on the information extracted.

3. The validation process will display the classification results, extracted information and validation results with the description of each validation rule and how it was applied.

4. (optional) Refresh the page if you want to analyze another set of documents

# POC NOTES
1. Only works on Airway Bills with perishable cargo. Analyzing Airway Bills containing non-perishable cargo will most likely result in a '✅ VALIDATION PASSED' outcome, however it is likely to be erroneous.

2. All of the validation rules are hardcoded based on interpretation of the information provided by IATA and their air carrier partners. Validation rules can be configured per each air carrier.

3. In future, a more sophisticated system which will automatically extract validation rules from the source regulation, as current POC has been designed to faciliate this architecture in the future.

4. A "high-precision" mode using additional input from an OCR Document Intellgigence can be implemented to encance the GPT4o text extraction ability

# TERMS OF USE
This is a proof of concept (POC) for demonstration and educational purposes only. It is not intended for production use and may contain bugs or incomplete features. This software is provided as-is, without warranty of any kind.