from flask import Flask, request
from flask_cors import CORS
from api_get_awb_content import read_awb, read_awb_base64
from api_required_docs import api_required_docs
from api_validate_docs_for_webui import api_upload_file_webui
from api_validate_docs import api_validate_docs
import configparser

app = Flask(__name__)

CORS(app)

# Define the folder where you want to save the uploaded files
app.config['UPLOAD_FOLDER'] = './uploads'

#----------------- APIs for Internal Web User Interface ----------------------
@app.route('/upload', methods=['POST'])
def upload_file():
    return api_upload_file_webui(request, app)

#----------------- APIs for External Consumption ------------------------------
@app.route('/uploadawb', methods=['POST'])
def read_awb():
    return read_awb(request, app)

@app.route('/uploadawb64', methods=['POST'])
def read_awb1():
    return read_awb_base64(request, app)

@app.route('/requireddocs', methods=['POST'])
def get_required_docs():
    return api_required_docs(request)

@app.route('/validatedocs', methods=['POST'])
def validate_docs():
    return api_validate_docs(request)


if __name__ == '__main__':
    # Run the Flask app

    config = configparser.ConfigParser()
    config.read('config.ini')
    server = config['DEFAULT']['Server']
    port = config['DEFAULT'].getint('Port')

    app.run(host=server, port=port) 

