import streamlit as st
import random
import importlib

user = st.session_state.user


MODEL_NAME_CLASS_DICT = {
    "xingchen": 'XingChen',
    "baichuan": "BaiChuan",
}

def get_model(server_name: str, model_name: str, api_key: str):
    server = importlib.import_module(f"libs.servers.{server_name}")
    ModelClass = getattr(server, MODEL_NAME_CLASS_DICT[model_name])
    model = ModelClass(api_key=api_key)
    return model

def chat(server_name, model_name, character_id, messages):
    api_key = random.choice(st.secrets[model_name])
    model = get_model(server_name, model_name, api_key)
    match model_name:
        case "xingchen":
            model = XingChen(api_key)
            message = messages[-1]['content']
            response = model.chat(
                character_id, message, seed=random.getrandbits(32), user_id=user.user_id
            )
            return response
        case "baichuan":
            api_key = st.secrets['baichuan_api_key']
            model = BaiChuan(api_key)
            response = model.chat(character_id, messages)
            return response



