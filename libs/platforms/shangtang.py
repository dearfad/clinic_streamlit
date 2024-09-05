import sensenova
import streamlit as st

sensenova.access_key_id = "B2366510AA0147BAB70C8C32FA0FC6FA"
sensenova.secret_access_key = "927DD0D163A74010A03007A7AEAE5BD4"

class ShangTang:
    def __init__(self, api_key) -> None:
        pass
    def chat(self, doctor, patient):
        response = sensenova.ChatCompletion.create(
            model=patient.model.model,
            max_new_tokens=1024,
            messages=patient.messages,
            repetition_penalty=1.05,
            temperature=0.8,
            top_p=0.7,
        )
        print(response)
        return response

