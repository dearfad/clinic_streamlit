from zhipuai import ZhipuAI
from libs.bvcutils import get_patient_info
from libs.bvcclasses import FakeProfile
from libs.bvcconst import SYSTEM_PROMPT


ZHIPU = "glm-4-flash"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_report",
            "description": "获取辅助检查的报告",
            "parameters": {
                "type": "object",
                "properties": {
                    "examination": {
                        "type": "string",
                        "description": "检查，例如：乳腺超声、血常规、心电",
                    },
                },
                "required": ["examination"],
            },
        },
    }
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
        if response.choices[0].message.tool_calls:
            tool_call = response.choices[0].message.tool_calls[0]
            args = eval(tool_call.function.arguments)
            if tool_call.function.name == "get_report":
                fakeprofile = FakeProfile()
                image = f"好的，这是我的{args['examination']} ![]({fakeprofile.photo.replace(" ", "%20")})"
                return image
        return response.choices[0].message.content
