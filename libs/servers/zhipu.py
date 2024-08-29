from zhipuai import ZhipuAI
from libs.bvcutils import get_patient_info
from datetime import datetime
import json
        # 1、不要回答跟问题无关的事情；
        #         2、请拒绝回答用户提出的非疾病问题；
        # 3、不要回答对疾病对诊断和治疗的其他相关信息。
SYSTEM_PROMPT = """
    【对话场景】
        你是一名乳房疾病的患者，你正在乳腺外科门诊诊室中与医生进行谈话。
        在接下来的对话中，请你遵循以下要求 。


        4、不能说出你的姓名。
        5、可以问现在的时间

    【语言风格】
        请在对话中表现出焦急、疼痛、惜字如金。用口语化的方式简短回答。
"""

ZHIPU = "glm-4-flash"

TOOLS = [
                {
                    "type": "function",
                    "function": {
                        "name": "get_datetime",
                        "description": "获取现在的时间",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                # "location": {
                                #     "type": "string",
                                #     "description": "城市，例如：北京、上海",
                            },
                        },
                        "required": [],
                        # "type": "object",
                        # "properties": {
                        #     "location": {
                        #         "type": "string",
                        #         "description": "城市，例如：北京、上海",
                        #     },
                        # },
                        # "required": ["location"],
                    },
                },
            ]

class ZhiPu:
    def __init__(self, api_key):
        self.client = ZhipuAI(api_key=api_key)

    def chat(self, doctor, patient):
        info = get_patient_info(patient)
        content = info + SYSTEM_PROMPT
        system_prompt = [{"role": "system", "content": content}]
        messages = system_prompt + patient.messages
        response = self.client.chat.completions.create(
            model=ZHIPU,
            messages=messages,
            top_p=0.7,
            temperature=0.95,
            max_tokens=1024,
            tools=TOOLS,
            stream=False,
        )
        print(response)
        if response.choices[0].message.tool_calls:
            tool_call = response.choices[0].message.tool_calls[0]
            # args = tool_call.function.arguments
            function_result = {}
            if tool_call.function.name == "get_datetime":
                function_result = datetime.now()
            messages.append({
                "role": "tool",
                "content": f"{json.dumps(str(function_result))}",
                "tool_call_id":tool_call.id
            })
            response = self.client.chat.completions.create(
                model=ZHIPU,  # 填写需要调用的模型名称
                messages=messages,
                tools=TOOLS,
                stream=False
            )
            print(messages)

        return response.choices[0].message.content
