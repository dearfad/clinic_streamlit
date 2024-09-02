from zhipuai import ZhipuAI
from libs.bvcutils import get_patient_info
from libs.bvcconst import SYSTEM_PROMPT, TOOLS


class ZhiPu:
    def __init__(self, api_key):
        self.client = ZhipuAI(api_key=api_key)

    def chat(self, doctor, patient):
        if patient.model.model == 'charglm-3':
            info = get_patient_info(patient)
            content = SYSTEM_PROMPT + info
            response = self.client.chat.completions.create(
                model=patient.model,
                meta = {
                    "user_info": "我是一名乳腺外科医生，现在正在乳腺外科门诊和患者谈话",
                    "bot_info": content,
                    "bot_name": "患者",
                    "user_name": "医生",
                },
                messages=patient.messages,
                top_p=0.7,
                temperature=0.95,
                max_tokens=1024,
                # tools=TOOLS,
                stream=False,
            )
        else:
            # info = get_patient_info(patient)
            # content = SYSTEM_PROMPT + info
            # system_prompt = [{"role": "system", "content": content}]
            # messages = system_prompt + patient.messages
            response = self.client.chat.completions.create(
                model=patient.model.model,
                messages=patient.messages,
                top_p=0.7,
                temperature=0.95,
                max_tokens=1024,
                # tools=TOOLS,
                stream=False,
            )
        # if response.choices[0].message.tool_calls:
        #     tool_call = response.choices[0].message.tool_calls[0]
        #     args = eval(tool_call.function.arguments)
        #     if tool_call.function.name == "get_report":
        #         fakeprofile = FakeProfile()
        #         image = f"好的，这是我的{args['examination']} ![]({fakeprofile.photo.replace(" ", "%20")})"
        #         return image
        # print(response)
        return response.choices[0].message.content
