from flask import Flask, request, jsonify
import os, json, base64
from read_doc_awb import get_awb_data
from read_doc_phyto import get_phyto_data
from read_doc_invoice import get_invoice_data
from prompt_resp_using_llm import are_documents_uploaded_valid
from find_coincidence import get_concidence_object_using_llm, get_concidence_object_using_llm_no_invoice


# Allow only certain types of files to be uploaded (optional)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def api_validate_docs(request):

    data = request.get_json()
    is_valid, message = validate_input(data)
    if not is_valid:
        return jsonify({"status": "error", "message": message}), 400

    files = data["files"]
    mandatoryDocsList = data.get("list_of_mandatory_documents", None)

    if mandatoryDocsList:
        mandatoryDocs = ", ".join(mandatoryDocsList)
    else:
        mandatoryDocs = "Air WayBill,Phytosanitary Document"

    print(f" Mandatory Docs : {mandatoryDocs}")

    awbFilePath     = ""
    phytoFilePath   = ""
    invoiceFilePath = ""
    other_docs      = []

    #--------------- Iterate through all the input files ----------------------------
    for item in files:
        document = save_input_doc(item)
        if 'error' in document:
            return document, 500
        
        if document['filetype'] == "Air WayBill" :
            awbFilePath = document["filepath"]

        if document['filetype'] == "Phytosanitary Certificate" :
            phytoFilePath = document["filepath"]

        if document['filetype'] == "Invoice" :
            invoiceFilePath = document["filepath"]

        if document['filetype'] != "Air WayBill" and document['filetype'] != "Phytosanitary Certificate" and document['filetype'] != "Invoice":
            other_docs.append(document["filetype"])

    # Process the saved file as needed
    result = validate_docs(awbFilePath, phytoFilePath, invoiceFilePath, other_docs, mandatoryDocs)

    return result, 200

def validate_input(data):
    
    # Check if files is present and contains at least one object
    if "files" not in data or not isinstance(data["files"], list) or len(data["files"]) == 0:
        return False, "Missing key: files or files list is empty"
    
    return True, "Input is valid"

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_awb_content_json(awb_file_path) :
    print("-------------Processing AWB for content extractions----------")
    awbObject = get_awb_data(awb_file_path, False)
    awbObject["isValid"] = is_awb_doc_valid(awbObject)
    return awbObject

def read_invoice_content_json(invoice_file_path) :
    print("-------------Processing Invoice for content extractions----------")
    invoiceObject = get_invoice_data(invoice_file_path)
    invoiceObject["isValid"] = is_invoice_doc_valid(invoiceObject)
    return invoiceObject

def is_invoice_doc_valid(awbObject) :
    if awbObject['Destination'] == 'NA':
        return False
    return True

def is_awb_doc_valid(awbObject) :
    if awbObject['origin'] == 'NA' or awbObject['destination'] == 'NA' :
        return False
    return True

def read_phyto_content_json(phyto_file_path) :
    # Read AWB Document
    print("-------------Processing Phyto for content extractions----------")
    phytoObject = get_phyto_data(phyto_file_path)
    phytoObject["isValid"] = is_phyto_doc_valid(phytoObject)
    return phytoObject

def is_phyto_doc_valid(phytoObject) :
    if phytoObject['origin'] == 'NA' or phytoObject['destination'] == 'NA' :
        return False
    return True

def is_document_available(files_saved, docName) :
    try:
        file_path = files_saved[docName]
        return True, file_path
    except Exception as e:
        return False, None


# Save object to file
def save_object(obj, filename):
    with open(filename, 'w') as f:
        json.dump(obj, f)

def validate_docs(awb_file_path, phyto_file_path, invoiceFilePath, other_docs, mandatoryDocs) :

    valid_docs = other_docs.copy()
    result = {}

    #---------------------------- Read AWB Contnt -------------------------
    try:
        # Code that may raise an exception
        awbContent = read_awb_content_json(awb_file_path)
    except Exception as e:
        print(f"Exception occurred while reading AWB content : {e}")
        awbContent = get_empty_awb_object()
        
    result['awb'] = awbContent

    if awbContent['isValid'] :
        valid_docs = ['Air Waybill']

    #---------------------------- Read Phyto Contnt -------------------------
    try:
        # Code that may raise an exception
        phytoContent = read_phyto_content_json(phyto_file_path)
    except Exception as e:
        print(f"Exception occurred while reading Phyto content : {e}")
        phytoContent = get_empty_phyto_object()
    
    result['phyto'] = phytoContent

    if phytoContent['isValid'] :
        valid_docs.append('Phytosanitary Certificate')

    #---------------------------- Read Invoice Contnt -------------------------
    try:
        # Code that may raise an exception
        invoiceContent = read_invoice_content_json(invoiceFilePath)
    except Exception as e:
        print(f"Exception occurred while reading Phyto content : {e}")
        invoiceContent = {"Destination":"NA", "isValid":False}

    if invoiceContent['isValid'] :
        valid_docs.append('Invoice')        

    #--------------------------- Handle Violations --------------------------
    if len(valid_docs) != 0:
        docs_provided = ",".join(valid_docs)
        print("-------------Validating for minimum document requirements----------")
        is_min_doc_requirement_met = are_documents_uploaded_valid(docs_provided, mandatoryDocs)
        result['mindocsrequirementmet'] = is_min_doc_requirement_met
        print(f"Minimum document requirement validation : {is_min_doc_requirement_met}")
    else:
        result['mindocsrequirementmet'] = ""
        print(f"Minimum document requirement validation : NA")    

    #------------------------- Handle Coincidence Check when Invoice present ----------------------------
    if awbContent['isValid'] and phytoContent['isValid'] and invoiceContent['isValid'] :
        try:
            # Code that may raise an exception
            print("-------------Processing Coincidence check with invoice ----------")
            concidenceObject = get_concidence_object_using_llm(awbContent, phytoContent, invoiceContent)
            result['conincidence'] = concidenceObject
        except Exception as e:
            result['conincidence'] = {}

        print(f" Coincident check : {concidenceObject}")

      #------------------------- Handle Coincidence Check when Invoice not present ----------------------------
    if awbContent['isValid'] and phytoContent['isValid'] and not invoiceContent['isValid'] :
        try:
            # Code that may raise an exception
            print("-------------Processing Coincidence check without invoice ----------")
            concidenceObject = get_concidence_object_using_llm_no_invoice(awbContent, phytoContent)
            result['conincidence'] = concidenceObject
        except Exception as e:
            result['conincidence'] = {}

        print(f" Coincident check : {concidenceObject}")

    return result

def get_empty_awb_object() :
    return {
            "Agent City": "NA",
            "Agent IATA Code": "NA",
            "Agent Name": "NA",
            "Consignee Address": "NA",
            "Consignee Name": "NA",
            "Executed On Date": "NA",
            "Shipper Address": "NA",
            "Shipper Name": "NA",
            "destination": "NA",
            "goodbeingtransported": "NA",
            "origin": "NA",
            "transit": "NA",
            "weight": "NA",
            "isValid": False
        }

def get_empty_phyto_object() :
    return{
            'origin': 'NA', 
            'destination' : 'NA',
            'date' : 'NA',
            'goodbeingtransported' : 'NA',
            'weight' : 'NA',
            "isValid": False             
        }

def save_input_doc(item) :

    print(f"File Name: {item['filename']}")
    print(f"File Type: {item['filetype']}")
    print()

    if 'filename' not in item or 'filedata' not in item:
        return {'error': 'No file data provided'}

    filename = item['filename']
    base64_awb_data = item['filedata']

    if not allowed_file(filename):
        return {'error': 'File type not allowed'}

    try:
        # Decode the base64 string
        awb_content_encoded = base64.b64decode(base64_awb_data)
    except base64.binascii.Error:
        return {'error': 'Invalid base64 encoding'}

    file_path = os.path.join("./uploads", filename)

    try:
        # Save the decoded file to the server
        with open(file_path, 'wb') as f:
            f.write(awb_content_encoded)
    except IOError:
        return {'error': 'Failed to save file'}
    
    result = item
    result['filepath'] = file_path
    
    return result

def get_sample_input() :
    sample_input_json = [
        {
            "filename" : "AWB.pdf",
            "filedata" : "asfsad",
            "filetype" : "Air WayBill"
        },
        {
            "filename" : "phyto.pdf",
            "filedata" : "asfsad",
            "filetype" : "Phytosanitary Certificate"
        }
    ]
    
    return sample_input_json

if __name__ == '__main__':
   
    sample_input_json = get_sample_input()

    


