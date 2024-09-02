from volcenginesdkarkruntime import Ark
from libs.bvcconst import SYSTEM_PROMPT
from libs.bvcutils import get_patient_info

MODEL = {
    "doubao-pro-4k": "ep-20240901112134-tzbfm",
    "doubao-lite-4k": "ep-20240901111140-wf7b5",
}


class ArkEngine:
    def __init__(self, api_key):
        self.client = Ark(
            api_key=api_key, base_url="https://ark.cn-beijing.volces.com/api/v3"
        )

    def chat(self, doctor, patient):
        # info = get_patient_info(patient)
        # content = "\n【你的病情】\n" + info + SYSTEM_PROMPT
        # system_prompt = [{"role": "system", "content": content}]
        # print(system_prompt)
        # messages = system_prompt + patient.messages
        completion = self.client.chat.completions.create(
            model=MODEL[patient.model.model],
            messages=patient.messages,
        )
        return completion.choices[0].message.content
