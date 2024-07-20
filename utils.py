import streamlit as st
import random
import pandas as pd
from xingchen import (
    Configuration,
    ApiClient,
    ChatApiSub,
    CharacterApiSub,
    ChatReqParams,
    CharacterKey,
    UserProfile,
)

PAGE_STYLE = """<style>
        header {visibility: hidden;}
        .block-container{
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        .st-emotion-cache-arzcut{
            padding-top: 1rem;
            padding-bottom: 1rem;
            padding-left: 3rem;
            padding-right: 3rem;
        }
        .stChatMessage{
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
        }
    </style>"""

ADMIN = 'DEARFAD'

############### READ DATA  ###################################
@st.cache_data
def read_cases(path):
    data = pd.read_json(path, orient='records')
    return data

#############################################################
class XingChen:
    configuration = Configuration(host="https://nlp.aliyuncs.com")
    configuration.access_token = "lm-bw72h4Q9oFOyuE47ncPxbg=="

    def __init__(self, character_id):
        with ApiClient(self.configuration) as api_client:
            self.chat_api = ChatApiSub(api_client)
            self.character_api = CharacterApiSub(api_client)
            self.user_id = str(random.randint(1, 1000))
            self.character_id = character_id
            # self.character = self.character_api.character_details(
            #     character_id=self.character_id
            # )
            # self.character_name = self.character.data.name
            # self.character_avatar = self.character.data.avatar

    def chat(self, messages):
        chat_param = ChatReqParams(
            bot_profile=CharacterKey(character_id=self.character_id),
            messages=messages,
            user_profile=UserProfile(user_id=self.user_id),
        )
        return self.chat_api.chat(chat_param).to_dict()["data"]["choices"][0][
            "messages"
        ][0]["content"]

    # character = st.session_state.character_api.character_details(
    #     character_id=st.session_state.character_id
    # )
    # st.session_state.patient_name = character.data.name
    # st.session_state.patient_avatar = character.data.avatar

    # col_left, col_center, col_right = st.columns(3)
    # with col_center:
    #     st.image(
    #         "http:" + st.session_state.patient_avatar.file_url,
    #         caption=st.session_state.patient_name,
    #         use_column_width=True,
    #     )


def BaiChuan():
    pass


def chat(role_server, character_id, messages):
    match role_server:
        case "xingchen":
            if "xingchen" not in st.session_state:
                xingchen = XingChen(character_id)
            return xingchen.chat(messages)
        case "baichuan":
            if "baichuan" not in st.session_state:
                baichuan = BaiChuan(character_id)
            return baichuan.chat(messages)

def get_cases(chapter):
    data = read_cases(f"cases/{chapter}.json")
    return data.sample(frac=1, ignore_index=True)
