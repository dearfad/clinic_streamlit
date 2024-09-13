import sensenova
import streamlit as st
from libs.bvcconst import TOOLS

def chat(patient):

    sensenova.access_key_id = st.secrets['shangtang_access_key_id']
    sensenova.secret_access_key = st.secrets['shangtang_secret_access_key']
    model = patient.model.name
    messages = patient.messages
    response = sensenova.ChatCompletion.create(
            model=model,
            # max_new_tokens=1024,
            messages=messages,
            # repetition_penalty=1.05,
            # temperature=0.8,
            # top_p=0.7,
            stream=False,
            tools=TOOLS,
        )
    print(response)
    if response.data.choices[0].get("tool_calls", None):
        tool_call = response.data.choices[0].tool_calls[0]
        args = eval(tool_call.function.arguments)
        if tool_call.function.name == "get_report":
            return f"好的，这是我的{args['report']} ![](app/static/乳腺超声.jpg)"
    return response.data.choices[0].message