import streamlit as st
from openai import OpenAI

from libs.bvcconst import TOOLS


def chat(patient):
    api_key = st.secrets[patient.model.module]
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    model = patient.model.name
    messages = patient.messages
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=False,
        tools=TOOLS,
        # temperature=1,
        # top_p=1,
    )
    if response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0]
        args = eval(tool_call.function.arguments)
        if tool_call.function.name == "get_report":
            return f"好的，这是我的{args['report']} ![](app/static/乳腺超声.jpg)"
    # print(response)
    return response.choices[0].message.content
