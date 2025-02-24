from prompt_resp_using_llm import get_answer, is_goods_perishable
import json

def get_concidence_object_using_llm(awbObject, phytoObject, invoiceObject):
    
    # Create a new object by copying the existing one
    newAwbObject = awbObject.copy()

    # Concatenate the values and update the new object
    newAwbObject["goodbeingtransported"] = (awbObject["Handling Information"] 
                                        + " " + awbObject["goodbeingtransported"]
                                      )
    prompt_concidence = """Given context consists of two JSON objects and it has few common attributes.
                        Please let me know if origin and destination attributes from both the objects
                        refer to same country even if the places are different. Don't answer No, if the
                        places are from the same country.
                        ( eg. 'UIO' airport and 'PICHINCHA' province are from Ecuador).
                        Please let me know if destination attributes from AWB and Phytosanitory and
                        invoice (if available) objects refer to the same airport location. 
                        Similarly if goodbeingtransported are same, consider that goods could be written 
                         in different languages between two objects and also two documents might contain
                         the different content for eg. first object may say flowers and the second object
                         says roses, but it refers to the same commodity.
                        And also compare weight attribute if it has the same value in AWB and Phytosanitory
                        discarding the format and detail.
                        Please provide the response in a json format, one attribute in the result JSON
                        for each of the compared attributes origin, destination,goodbeingtransported and 
                        weight.
                       Please provide Yes or No and some explanation for each attribute not exceeding 50 words 
                        and do include the values of the attributes as well if possible.
                        Resulting response should be in proper JSON format and provide only the JSON content
                          and no other content especially '''json'''"""
    
    context_messages = [f"AWB JSON Object : {newAwbObject}"]
    context_messages.append(f"Phytosanitory JSON Object : {phytoObject}")
    context_messages.append(f"Invoice JSON Object : {invoiceObject}")

    answerObject = get_answer(prompt_concidence, context_messages)

    json_object = json.loads(answerObject)
   
    json_object1 = json_object["choices"][0]["message"]["content"]  

    return json.loads(json_object1)

def get_concidence_object_using_llm_no_invoice(awbObject, phytoObject):
    
    # Create a new object by copying the existing one
    newAwbObject = awbObject.copy()

    # Concatenate the values and update the new object
    newAwbObject["goodbeingtransported"] = (awbObject["Handling Information"] 
                                        + " " + awbObject["goodbeingtransported"]
                                      ) 

    prompt_concidence = """Given context consists of two JSON objects and it has few common attributes.
                        Please let me know if origin and destination attributes from both the objects
                        refer to same country even if the places are different. Don't answer No, if the
                        places are from the same country.
                        ( eg. 'UIO' airport and 'PICHINCHA' province are from Ecuador).
                        Similarly if goodbeingtransported are same, consider that goods could be written 
                         in different languages between two objects and also two documents might contain
                         the different content for eg. first object may say flowers and the second object
                         says roses, but it refers to the same commodity.
                        And also compare weight attribute if it has the same value discarding the format and detail.
                        Please provide the response in a json format, one attribute in the result JSON
                        for each of the compared attributes origin, destination,goodbeingtransported and 
                        weight. Also when one of the object's attribute value consists of value NA, 
                        please provide the answer Yes.
                        Please provide Yes or No and some explanation for each attribute not exceeding 50 words 
                        and do include the values of the attributes as well if possible.
                        Resulting response should be in proper JSON format and provide only the JSON content
                          and no other content especially '''json'''"""
    
    context_messages = [f"AWB JSON Object : {newAwbObject}"]
    context_messages.append(f"Phytosanitory JSON Object : {phytoObject}")

    answerObject = get_answer(prompt_concidence, context_messages)

    json_object = json.loads(answerObject)
   
    json_object1 = json_object["choices"][0]["message"]["content"]  

    return json.loads(json_object1)