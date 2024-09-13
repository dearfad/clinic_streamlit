import sensenova
import streamlit as st

sensenova.access_key_id = st.secrets['shangtang_access_key_id']
sensenova.secret_access_key = st.secrets['shangtang_secret_access_key']

def chat(patient):
    model = patient.model.name
    messages = patient.messages
    response = sensenova.ChatCompletion.create(
            model=model,
            # max_new_tokens=1024,
            messages=messages,
            # repetition_penalty=1.05,
            # temperature=0.8,
            # top_p=0.7,
        )
    print(response)
    return response