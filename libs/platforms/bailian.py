from http import HTTPStatus

import dashscope

from libs.bvcconst import SYSTEM_PROMPT, TOOLS
from libs.bvcutils import get_patient_info

def get_doctor_info():
    return "doctor_info"

def get_report():
    return "report"


class BaiLian:
    def __init__(self, api_key):
        dashscope.api_key = api_key

    def chat(self, doctor, patient):
        # info = get_patient_info(patient)
        # content = info + SYSTEM_PROMPT
        # system_prompt = [{"role": "system", "content": content}]
        # messages = system_prompt + patient.messages
        response = dashscope.Generation.call(
            model=patient.model.model,
            messages=patient.messages,
            # tools=TOOLS,
            result_format="message",
        )
        if response.status_code == HTTPStatus.OK:
            # if response.output.choices[0]["message"].get("tool_calls", None):
            #     tool = response.output.choices[0]["message"]["tool_calls"][0]['function']['name']
            #     args = response.output.choices[0]["message"]["tool_calls"][0]['function']['arguments']                
            #     if tool == 'get_doctor_info':                    
            #         return response.output.choices[0]["message"]["content"] + get_doctor_info() + args
            #     elif tool == "get_report":
            #         return response.output.choices[0]["message"]["content"] + get_report() + args
            #     else:
            #         return response.output.choices[0]["message"]["content"] + "Unknown tool" + args
            # else:
            #     return response.output.choices[0]["message"]["content"]
            return response.output.choices[0]["message"]["content"]
        else:
            return f"Request id: {response.request_id}, Status code: {response.status_code}, error code: {response.code}, error message: {response.message}"
