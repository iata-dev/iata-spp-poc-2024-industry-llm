from flask import Flask, request, jsonify
from read_doc_awb import get_awb_data
import os
import base64

# Allow only certain types of files to be uploaded (optional)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_awb_base64(request, app):

    data = request.get_json()

    if 'filename' not in data or 'filedata' not in data:
        return jsonify({'error': 'No file data provided'}), 400

    filename = data['filename']
    filedata = data['filedata']

    if not allowed_file(filename):
        return jsonify({'error': 'File type not allowed'}), 400

    try:
        # Decode the base64 string
        file_bytes = base64.b64decode(filedata)
    except base64.binascii.Error:
        return jsonify({'error': 'Invalid base64 encoding'}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(file_path)

    try:
        # Save the decoded file to the server
        with open(file_path, 'wb') as f:
            f.write(file_bytes)
    except IOError:
        return jsonify({'error': 'Failed to save file'}), 500

    # Process the saved file as needed
    # For example, call your get_awb_data function
    try:
        # Code that may raise an exception
        awb_object = get_awb_data(file_path, False)
    except Exception as e:
        print(f"Exception occurred while reading AWB content : {e}")
        awb_object = get_empty_awb_object()

    return jsonify(awb_object), 200

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

def read_awb(request, app):
   
    # Save files locally to uploads folder
   
    file = request.files['file']
    filePath = ''
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filePath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filePath)
        

    result = {}

    # Read AWB Document    
    print("-------------Processing AWB for content extractions----------")
    awbObject = get_awb_data(filePath)
    if awbObject is not None:
        result = awbObject    

    return jsonify(result), 200