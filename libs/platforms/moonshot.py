from openai import OpenAI
from libs.bvcutils import get_patient_info, build_system_prompt
from libs.bvcconst import SYSTEM_PROMPT

class MoonShot:
    def __init__(self, api_key):
        self.client = OpenAI(
    api_key=api_key,
    base_url="https://api.moonshot.cn/v1",
)
    def chat(self, doctor, patient):
        # info = get_patient_info(patient)
        # content = SYSTEM_PROMPT + info
        # system_prompt = [{"role": "system", "content": content}]
        # system_prompt = build_system_prompt(patient)
        # messages = system_prompt + patient.messages
        response = self.client.chat.completions.create(
            model = patient.model.model,
            messages = patient.messages,
            # temperature = 0.9,
        )
        # print(response)
        
        return response.choices[0].message.content