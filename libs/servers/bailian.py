import dashscope
from libs.bvcconst import SYSTEM_PROMPT
from libs.bvcutils import get_patient_info

class BaiLian:
    def __init__(self, api_key):
        dashscope.api_key = api_key

    def chat(self, doctor, patient):
        info = get_patient_info(patient)
        content = info + SYSTEM_PROMPT
        system_prompt = [{"role": "system", "content": content}]
        response = dashscope.Generation.call(
            model=patient.model,
            messages=system_prompt + patient.messages,
            result_format="message",
        )
        return response.output.choices[0]["message"]["content"]