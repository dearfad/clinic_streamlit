import streamlit as st
from openai import OpenAI

# from libs.bvcconst import TOOLS


def chat(model: str, messages: list) -> str:
    client = OpenAI(
        api_key=st.secrets["bailian"],
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=False,
        # tools=TOOLS,
        # temperature=1,
        # top_p=0.8,
    )
    # print(response)
    # if response.choices[0].message.tool_calls:
    #     tool_call = response.choices[0].message.tool_calls[0]
    #     args = eval(tool_call.function.arguments)
    #     if tool_call.function.name == "get_report":
    #         return f"好的，这是我的{args['report']} ![](app/static/乳腺超声.jpg)"
    return response.choices[0].message.content
