from zhipuai import ZhipuAI
from libs.bvcconst import TOOLS


class ZhiPu:
    def __init__(self, api_key):
        self.client = ZhipuAI(api_key=api_key)

    def chat(self, doctor, patient):
        response = self.client.chat.completions.create(
            model=patient.model.model,
            messages=patient.messages,
            tools=TOOLS,
            # temperature=0.1,
        )
        if response.choices[0].message.tool_calls:
            tool_call = response.choices[0].message.tool_calls[0]
            args = eval(tool_call.function.arguments)
            if tool_call.function.name == "get_report_id":
                return f"好的，这是我的{args['report']} ![](app/static/乳腺超声.jpg)"
        print(response)
        return response.choices[0].message.content
