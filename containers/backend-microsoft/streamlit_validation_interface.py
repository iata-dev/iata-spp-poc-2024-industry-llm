import streamlit as st
import threading
import time
import base64
from PIL import Image
from dotenv import load_dotenv
from validaton_backend import *
import os
os.environ["PYDEVD_WARN_EVALUATION_TIMEOUT"] = "10"

# set the environment variables needed to call the GPT4o model deployed to Azure OpenAI
load_dotenv(override=True)

progress_lock = threading.Lock()
progress_data = {}

def thread_safe_progress_callback(data, message, new_message=True):
    with progress_lock:
        if progress_data.get('new_message', False) == True:
                time.sleep(0.3)
        else:
            progress_data['data'] = data
            progress_data['message'] = message
            progress_data['new_message'] = new_message
        time.sleep(0.3)


def run_validation(input_list_of_dict_doc_pages):
    validation_thread = threading.Thread(target=visual_prompt_validate_documents, args=(input_list_of_dict_doc_pages, thread_safe_progress_callback))
    validation_thread.start()

st.expander("Instructions", expanded=False).markdown("# Instructions\n 1. Upload a set of airway bill documents in PDF format. You can upload multiple files and each file can contain multiple documents related to the airway bill. \n\n2. Click the 'Validate Documents' button to start the validation process.\n\n3. The validation process will classify the documents, extract information and validate the documents against a set of validation rules that are dynamically determined as appropriate based on the information extracted.\n\n4. The validation process will display the classification results, extracted information and validation results with the description of each validation rule and how it was applied.\n\n 5. (optional) Refresh the page if you want to analyze another set of documents \n\n # POC notes \n\n 1. Only works on Airway Bills with perishable cargo. Analyzing Airway Bills containing non-perishable cargo will most likely result in a ':white_check_mark: :green[VALIDATION PASSED]' outcome, however it is likely to be erroneous. \n\n 2. All of the validation rules are hardcoded based on interpretation of the information provided by IATA. A more sophisticated system which will automatically extract validation rules from the source regulation has been proposed and the current POC has been designed to faciliate this architecture in the future. \n\n # Terms of use \n\nThis is a proof of concept (POC) for demonstration and educational purposes only. It is not intended for production use and may contain bugs or incomplete features. This software is provided as-is, without warranty of any kind. \n\n ")

uploaded_files = st.file_uploader(
    "Upload airway bill document set in PDF format", accept_multiple_files=True
)

submitted_documents_dict = {}
input_image_list = []
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    image_list = pdf_to_base64_jpeg([bytes_data], uploaded_file.name)
    input_image_list.extend(image_list)
    # On the last iteration, set the `submitted_documents_dict` to be used in the validation process
    if uploaded_file == uploaded_files[-1]:
        submitted_documents_dict = {'input_image_list':input_image_list}

# create a streamlit container for each image
st_container_dict = {}
for image_list in input_image_list:
    st_container_dict[image_list['document_entity_name']] = st.container(border=True)


markdown_returned = None

if st.button("Validate Documents", disabled=not bool(submitted_documents_dict)):
    
    container_validation_final = st.container(border=True)
    validation_ongoing = True

    run_validation(submitted_documents_dict)
    with st.spinner("Validating Airway bill documents..."):
        while validation_ongoing:
            with progress_lock:
                if 'new_message' in progress_data and progress_data['new_message'] is True:
                    if progress_data['message'] == 'classification':

                        #set the container where to display the classification results
                        file_name_page = progress_data['data']['document_entity_name']
                        st_container_file_name_page = st_container_dict[file_name_page]

                        #composing markdown to display the image and classification results
                        #get the base64 image and convert it to an image
                        base64_image = progress_data['data']['image_base64']
                        # Decode the Base64 string
                        image_data = base64.b64decode(base64_image)
                        # Convert the bytes to an image
                        image_to_display = Image.open(BytesIO(image_data))    

                        # classification results LLM_visual_document_type
                        document_type_class = progress_data['data']['LLM_visual_document_type']
                        document_type_COT = progress_data['data']['LLM_visual_document_type_COT']
                        document_language = progress_data['data']['LLM_visual_document_language']

                        classification_markdown = f"**:orange[Document classification result]**: {document_type_class} \n\n **:orange[Classification decision explanation]**: {document_type_COT} \n\n **:orange[Language detected]**: {document_language} \n\n"
                        
                        with st_container_file_name_page:
                            st.image(image_to_display, use_container_width=True)
                        st_container_file_name_page.markdown(f"#### :orange[Document classification] \n\n")
                        st_container_file_name_page.markdown(f"**:orange[Document analyzed]**: {file_name_page}")
                        st_container_file_name_page.markdown(classification_markdown)

                        # indicate that the message has been displayed
                        progress_data['new_message'] = False

                    if progress_data['message'] == 'extraction':

                        #set the container to display the classification results
                        file_name_page = progress_data['data']['document_entity_name']
                        st_container_file_name_page = st_container_dict[file_name_page]

                        extracted_details = progress_data['data']['LLM_visual_extracted_details']
                        
                        markdown_extracted_details = f"#### :blue[Document data extracted] \n\n"
                        for key, value in extracted_details.items():
                            # if isinstance(value, list):
                            #     markdown_extracted_details += f"**:blue[{key}]**:\n\n"
                            #     for item_dict in value:
                            #         for key1, value1 in item_dict.items():
                            #             markdown_extracted_details += f"- **:green[{key1}]**: {value1} \n\n"
                            # else:
                            markdown_extracted_details += f"**:blue[{key}]**:\n {value} \n\n"
                        
                        st_container_file_name_page.markdown(markdown_extracted_details)

                        # indicate that the message has been displayed
                        progress_data['new_message'] = False

                    if progress_data['message'] == 'validation':
                        final_validation_pass = progress_data['data']['final_validated_passed_check']
                        validation_rules_markdown = progress_data['data']['validation_result_markdown']

                        if final_validation_pass:
                            validation_rules_markdown = f"## :white_check_mark: :green[VALIDATION PASSED] \n\n *view applied :violet[validation rules] below* \n\n --- \n\n {validation_rules_markdown}"
                        else:
                            validation_rules_markdown = f"## :x: :red[VALIDATION FAILED] \n\n *view applied :violet[validation rules] below* \n\n --- \n\n {validation_rules_markdown}"

                        container_validation_final.markdown(validation_rules_markdown)

                        # print total tokens spent
                        total_tokens_combined = progress_data['data']['total_tokens_combined']
                        total_tokens_input = progress_data['data']['total_tokens_prompt']
                        total_tokens_output = progress_data['data']['total_tokens_completion']
                        processing_time = round(progress_data['data']['processing_time'],1)

                        container_validation_final.markdown(f"\n\n #### Processing statistics:\n\n GPT4o tokens spent total={total_tokens_combined}  (input= {total_tokens_input} + output={total_tokens_output}) \n\n Processing time: {processing_time} seconds. #### Total cost: \n\n ${round((0.0000025 * total_tokens_input) + (0.00001 * total_tokens_output),4)} USD ([pay-as-you-go](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/#pricing), with no commitment):  \n\n ${round(((0.0000025 * total_tokens_input) + (0.00001 * total_tokens_output)*0.81),4)} USD ([PTU](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/provisioned-throughput?tabs=global-ptum), with commitment):  \n\n\n\n The total cost given above is an approximation. \n Actual cost will depend on the size of commitment, location and type of deployment. \n\n ")


                        # trigger the end of the validation process
                        validation_ongoing = False

            time.sleep(0.3)