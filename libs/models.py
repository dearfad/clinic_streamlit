import streamlit as st
import random

from libs.servers.tongyi import XingChen

user = st.session_state.user


def chat(model_name, character_id, message):
    match model_name:
        case "xingchen":
            api_key = random.choice(st.secrets["xingchen_api_keys"])
            model = XingChen(api_key)
            response = model.chat(
                character_id, message, seed=random.getrandbits(32), user_id=user.user_id
            )
            return response
        case "baichuan":
            pass
