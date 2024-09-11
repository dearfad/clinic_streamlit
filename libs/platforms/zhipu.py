import streamlit as st
from zhipuai import ZhipuAI

from libs.bvcconst import TOOLS


def chat(patient):
    api_key = st.secrets['zhipu']
    client = ZhipuAI(api_key=api_key)
    model = patient.model.name
    messages = patient.messages
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=False,
        tools=TOOLS,
        # temperature=0.95,
        # top_p=0.7,
    )
    if response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0]
        args = eval(tool_call.function.arguments)
        if tool_call.function.name == "get_report":
            return f"好的，这是我的{args['report']} ![](app/static/乳腺超声.jpg)"
    # print(response)
    return response.choices[0].message.content
