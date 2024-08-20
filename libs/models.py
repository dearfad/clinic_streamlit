import streamlit as st
import random

from libs.servers.tongyi import XingChen
from libs.servers.baichuan import BaiChuan

user = st.session_state.user

def chat(model_name, character_id, messages):
    match model_name:
        case "xingchen":
            api_key = random.choice(st.secrets["xingchen_api_keys"])
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
