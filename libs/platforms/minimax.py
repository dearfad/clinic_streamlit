import streamlit as st
from openai import OpenAI

# parameters: str not dict
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_report",
            "description": "如果用户想看一下检查报告时应用",
            "parameters": '{"type":"object", "properties":{"report":{"type":"string", "description":"检查报告，如：超声，血常规等"}}, "required":["report"]}',
        },
    }
]


def chat(patient):
    api_key = st.secrets["minimax"]
    client = OpenAI(api_key=api_key, base_url="https://api.minimax.chat/v1")
    model = patient.model.name
    messages = patient.messages
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=False,
        tools=tools,
        # tool_choice= "auto",
        # temperature=1,
        # top_p=1,
    )
    # print(response)
    if response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0]
        args = eval(tool_call.function.arguments)
        if tool_call.function.name == "get_report":
            return f"好的，这是我的{args['report']} ![](app/static/乳腺超声.jpg)"
    return response.choices[0].message.content
