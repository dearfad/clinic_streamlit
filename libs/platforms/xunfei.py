import streamlit as st
from openai import OpenAI

from libs.bvcconst import TOOLS

MODEL = {
    "Spark Lite": "general",
    "Spark Pro": "generalv3",
    "Spark Max": "generalv3.5",
    "Spark Ultra": "4.0Ultra",
}

def chat(patient):
    api_key = st.secrets['xunfei']
    client = OpenAI(api_key=api_key, base_url="https://spark-api-open.xf-yun.com/v1")
    model = patient.model.name
    messages = patient.messages
    response = client.chat.completions.create(
        model=MODEL[model],
        messages=messages,
        stream=False,
        tools=TOOLS,
        # temperature=1,
        # top_p=1,
    )
    print(response)
    if response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls
        args = eval(tool_call['function']['arguments'])
        if tool_call['function']['name'] == "get_report":
            return f"好的，这是我的{args['report']} ![](app/static/乳腺超声.jpg)"
    return response.choices[0].message.content
