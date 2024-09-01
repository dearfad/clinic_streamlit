from openai import OpenAI
from libs.bvcutils import get_patient_info
from libs.bvcconst import SYSTEM_PROMPT

class MiniMax:
    def __init__(self, api_key) -> None:
        self.client = OpenAI(api_key=api_key, base_url="https://api.minimax.chat/v1")

    def chat(self, doctor, patient):
        info = get_patient_info(patient)
        content = "\n【你的病情】\n" + info + SYSTEM_PROMPT
        system_prompt = [{"role": "system", "content": content}]
        print(system_prompt)
        messages = system_prompt + patient.messages
        response = self.client.chat.completions.create(
            model="abab6.5s-chat",
            messages=messages,
            stream=False,
        )
        print(response)
        return  response.choices[0].message.content
