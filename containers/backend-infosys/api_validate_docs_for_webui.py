from flask import Flask, request, jsonify
import os, json
from read_doc_awb import get_awb_data
from read_doc_phyto import get_phyto_data
from prompt_resp_using_llm import are_documents_uploaded_valid
from validate_violations import get_all_applicable_violations


# Allow only certain types of files to be uploaded (optional)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def api_upload_file_webui(request, app):
   
    # Save files locally to uploads folder
    files_saved = {}
    totalFiles = request.form.get('totalFiles', type=int)

    for i in range(totalFiles):
        file = request.files[f'file{i}']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file and allowed_file(file.filename):
            filePath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filePath)
            fileType = request.form.get(f'fileType{i}')
            print(f'File Type : {fileType} - {filePath}')
            files_saved[fileType] = filePath

    result = {}
    result['docsreadable'] = []
    result['docsprovided'] = list(files_saved.keys())
    valid_docs = []

    # Read AWB Document
    is_awb_availabe, awb_file_path = is_document_available(files_saved, 'Air WayBill')
    awbObject = {}
    if is_awb_availabe :
        print("-------------Processing AWB for content extractions----------")
        awbObject = get_awb_data(awb_file_path,True)
        if awbObject is not None:
            #save_object(awbObject, AWB_JSON_LOCATION)        
            result['docsreadable'].append('Air WayBill: Yes')
            valid_docs.append('Air WayBill')
            result['awb'] = awbObject
        else :
            result['docsreadable'].append('Air WayBill: No')
            result['awb'] = get_empty_awb_object()
    else :
        result['docsreadable'].append('Air WayBill: No')
        result['awb'] = get_empty_awb_object()
    
    # Read Phytosanitory Certificate  
    is_phyto_availabe, phyto_file_path = is_document_available(files_saved, 'Phytosanitory')
    phytoObject = {}
    if is_phyto_availabe :
        print("-------------Processing Phytosanitory certificate for content extractions----------")
        phytoObject = get_phyto_data(phyto_file_path)
        if phytoObject is not None:  
            result['docsreadable'].append('Phytosanitory: Yes')
            valid_docs.append('Phytosanitary certificate')
            result['phyto'] = phytoObject
        else :
            result['docsreadable'].append('Phytosanitory: No')
            result['phyto'] = get_empty_phyto_object()
    else :
        result['phyto'] = get_empty_phyto_object()

    #--------------------------- Handle Violations --------------------------
    docs_provided = ",".join(valid_docs)
    print("-------------Validating for minimum document requirements----------")
    is_min_doc_requirement_met = are_documents_uploaded_valid(docs_provided)
    result['violations'] = []
    print(is_min_doc_requirement_met)
    result['violations'].append(is_min_doc_requirement_met)
    if is_awb_availabe :
        violations = get_all_applicable_violations(awb_file_path)

        for violation in violations:
            result['violations'].append(violation)

    #--------------------------- Handle Conicidence --------------------------
    
    if awbObject and phytoObject and False:
        print("-------------Processing Coincidence check ----------")
        result['coincidence'] = {}
        result['coincidence']['origin'] = is_origin_conicidence(awbObject['origin'], 
                                                                    phytoObject['origin'])
        result['coincidence']['destination'] = is_origin_conicidence(awbObject['destination'], 
                                                                    phytoObject['destination'])
        result['coincidence']['goods'] = is_origin_conicidence(awbObject['goodbeingtransported'], 
                                                                    phytoObject['goodbeingtransported'])
        result['coincidence']['weight'] = is_origin_conicidence(awbObject['weight'], 
                                                                    phytoObject['weight'])
    else:
        print("------------- Skipping Processing Coincidence check for perf reasons ----------")
        result['coincidence'] = {}
        result['coincidence']['origin'] = 'NA'
        result['coincidence']['destination'] = 'NA'
        result['coincidence']['goods'] = 'NA'
        result['coincidence']['weight'] = 'NA'

    return jsonify(result), 200

def is_document_available(files_saved, docName) :
    try:
        file_path = files_saved[docName]
        return True, file_path
    except Exception as e:
        return False, None

def get_empty_phyto_object() :
    return{
            'origin': 'NA', 
            'destination' : 'NA',
            'date' : 'NA',
            'goodbeingtransported' : 'NA',
            'weight' : 'NA',             
        }

def get_empty_awb_object() :
   return  {
            'origin': 'NA', 
            'destination' : 'NA',
            'transit' : 'NA',
            'date' : 'NA',
            'goodbeingtransported' : 'NA',
            'weight' : 'NA', 
            'classofgoods' : 'NA'
        }
        

# Save object to file
def save_object(obj, filename):
    with open(filename, 'w') as f:
        json.dump(obj, f)