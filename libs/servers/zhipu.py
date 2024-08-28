from zhipuai import ZhipuAI
from libs.bvcutils import get_patient_info

SYSTEM_PROMPT = """
    【对话场景】
        你是一名乳房疾病的患者，你正在乳腺外科门诊诊室中与医生进行谈话。在接下来的对话中，请你遵循以下要求 。1、不要回答跟问题无关的事情；2、请拒绝回答用户提出的非疾病问题；3、不要回答对疾病对诊断和治疗的其他相关信息。4、不能说出你的姓名。

    【语言风格】
        请在对话中表现出焦急、疼痛、惜字如金。用口语化的方式简短回答。
"""

ZHIPU = "glm-4-flash"


class ZhiPu:
    def __init__(self, api_key):
        self.client = ZhipuAI(api_key=api_key)

    def chat(self, doctor, patient):
        info = get_patient_info(patient)
        content = info + SYSTEM_PROMPT
        system_prompt = [{"role": "system", "content": content}]
        response = self.client.chat.completions.create(
            model=ZHIPU,
            messages=system_prompt + patient.messages,
            top_p=0.7,
            temperature=0.95,
            max_tokens=1024,
            stream=False,
        )
        return str(response.choices[0].message.content)
