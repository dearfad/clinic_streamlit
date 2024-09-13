import streamlit as st
from openai import OpenAI

from libs.bvcconst import TOOLS

MODEL = {
    "doubao-pro-4k": "ep-20240913120313-j764t",  #character-240728
    "doubao-pro-32k": "ep-20240913081755-mlqbh",
    "doubao-pro-128k": "ep-20240913081920-xfbt5",
    # "doubao-lite-4k": "ep-20240913083907-cmvgr", # character-240515
    # "doubao-lite-4k": "ep-20240913095618-mp7wv", # character-240828
    "doubao-lite-4k": "ep-20240913101031-7ghgj", # 240328
    "doubao-lite-32k": "ep-20240913082027-zrd5f",
    "doubao-lite-128k": "ep-20240913082052-st5hh",
}


def chat(patient):
    api_key = st.secrets["arkengine"]
    client = OpenAI(
        api_key=api_key, base_url="https://ark.cn-beijing.volces.com/api/v3"
    )
    model = patient.model.name
    messages = patient.messages
    response = client.chat.completions.create(
        model=MODEL[model],
        messages=messages,
        stream=False,
        tools=TOOLS,
        # temperature=1,
        # top_p=0.8,
    )
    # print(response)
    if response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0]
        args = eval(tool_call.function.arguments)
        if tool_call.function.name == "get_report":
            return f"好的，这是我的{args['report']} ![](app/static/乳腺超声.jpg)"
    return response.choices[0].message.content
