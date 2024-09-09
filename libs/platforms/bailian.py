from http import HTTPStatus

import dashscope

from libs.bvcconst import TOOLS


class BaiLian:
    def __init__(self, api_key):
        dashscope.api_key = api_key

    def chat(self, doctor, patient):
        response = dashscope.Generation.call(
            model=patient.model.model,
            messages=patient.messages,
            tools=TOOLS,
            result_format="message",
        )
        if response.status_code == HTTPStatus.OK:
            # print(response)
            if response.output.choices[0]["message"].get("tool_calls", None):
                tool_call = response.output.choices[0]["message"]["tool_calls"][0]
                args = eval(tool_call['function']['arguments'])
                if tool_call['function']['name'] == "get_report":
                    return (
                        f"好的，这是我的{args['report']} ![](app/static/乳腺超声.jpg)"
                    )
            return response.output.choices[0]["message"]["content"]
        else:
            return f"Request id: {response.request_id}, Status code: {response.status_code}, error code: {response.code}, error message: {response.message}"
