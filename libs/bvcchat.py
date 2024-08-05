import streamlit as st
import random
from xingchen import (
    Configuration,
    ApiClient,
    ChatApiSub,
    CharacterApiSub,
    ChatReqParams,
    CharacterKey,
    UserProfile,
)

class XingChen:
    configuration = Configuration(host="https://nlp.aliyuncs.com")
    configuration.access_token = "lm-bw72h4Q9oFOyuE47ncPxbg=="

    def __init__(self, character_id):
        with ApiClient(self.configuration) as api_client:
            self.chat_api = ChatApiSub(api_client)
            self.character_api = CharacterApiSub(api_client)
            self.user_id = str(random.randint(1, 1000))
            self.character_id = character_id

    def chat(self, messages):
        chat_param = ChatReqParams(
            bot_profile=CharacterKey(character_id=self.character_id),
            messages=messages,
            user_profile=UserProfile(user_id=self.user_id),
        )
        try:
            response = self.chat_api.chat(chat_param).to_dict()
            if response["success"]:
                return response["data"]["choices"][0]["messages"][0]["content"]
            else:
                return (
                    f"( 似乎自己在思索什么，嘴里反复说着数字 ~ {response['code']} ~ )"
                )
        except Exception as exception:
            return f"( 脑子坏掉了，等会再问我吧 ~ 原因是: {exception})"

    def detail(self):
        self.character = self.character_api.character_details(
            character_id=self.character_id
        )
        self.character_name = self.character.data.name
        self.character_avatar_url = "http:" + self.character.data.avatar.file_url


def BaiChuan():
    def __init__(self):
        pass

    def chat(self, messages):
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