from prompt_resp_using_llm import get_answer
import json
from read_doc_using_di import get_content_using_di
import validate_cites
import validate_dryice
import validate_perishable

 
def are_goods_perishable(awbContent, prompt_reqired_goods_available) :

    answerObject = get_answer(input_query=prompt_reqired_goods_available, context_messages=[awbContent])

    json_object = json.loads(answerObject)

    response = json_object["choices"][0]["message"]["content"]

    if "Yes" in response:
        return True
    else:
        return False
    
def get_violation_content(file_path, prompts) :

    awbContent = get_content_using_di(file_path)

    if are_goods_perishable(awbContent, prompts["requiredgoodsavailable"]) :       

        context_messages = [f"Air WayBill Content: {awbContent } "]
        context_messages.append(f"""Regulatory Requirements: {prompts["rules"]}""")
        
        answerObject = get_answer(input_query=prompts["violationcheck"], context_messages=context_messages)

        json_object = json.loads(answerObject)

        return json_object["choices"][0]["message"]["content"]
    else:
        return ""

def get_all_applicable_violations(file_path) :

    violations = []

    if "AWB_Violation_Perishable" in file_path :
        print(f"------------------ Executing the perishable violations check - {file_path}")
        # --------------------- Perishable Goods Violations --------------------------------
        prompts =  {
            "rules" : validate_perishable.rules,
            "requiredgoodsavailable" : validate_perishable.prompt_reqired_goods_available,
            "violationcheck" : validate_perishable.prompt_violation_check
        }
        
        violation_content = get_violation_content(file_path, prompts)

        if violation_content :
            violations.append(violation_content)
    
       
    if "AWB_WITH_DRY_ICE" in file_path :
        print(f"------------------ Executing the Dry ICE violations check - {file_path}")
        # -------------------- Dry ICE related violations ---------------------------------
        prompts =  {
            "rules" : validate_dryice.rules,
            "requiredgoodsavailable" : validate_dryice.prompt_reqired_goods_available,
            "violationcheck" : validate_dryice.prompt_violation_check
        }
        
        violation_content = get_violation_content(file_path, prompts)

        if violation_content :
            violations.append(violation_content)
    
    if "AWB_PEA_CITESNeeded" in file_path :
        print(f"------------------ Executing the CITES violations check - {file_path}")
        # -------------------- CITES related violations ---------------------------------
        prompts =  {
            "rules" : validate_cites.rules,
            "requiredgoodsavailable" : validate_cites.prompt_reqired_goods_available,
            "violationcheck" : validate_cites.prompt_violation_check
        }
        
        violation_content = get_violation_content(file_path, prompts)

        if violation_content :
            violations.append(violation_content)
    

    return violations

def contains_any(string, substrings):
    return any(substring in string for substring in substrings)



if __name__ == "__main__":

    file_path = r"C:\Users\bhanumurthi_t\OneDrive - Infosys Limited\Desktop\IATA POC\IATA PoC data\TestAWB\AWB_WITH_DRY_ICE.pdf"

    violations = get_all_applicable_violations(file_path)

    for violation in violations:
        print(f"---> {violation}")
