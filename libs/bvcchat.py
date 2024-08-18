import streamlit as st
import uuid
import pandas as pd
from xingchen import (
    Configuration,
    ApiClient,
    ChatApiSub,
    CharacterApiSub,
    CharacterQueryDTO,
    CharacterQueryWhere,
    ChatReqParams,
    CharacterKey,
    UserProfile,
)

class XingChen:
    configuration = Configuration(host="https://nlp.aliyuncs.com")
    configuration.access_token = st.secrets['xingchen_token']

    def __init__(self):
        with ApiClient(self.configuration) as api_client:
            self.chat_api = ChatApiSub(api_client)
            self.character_api = CharacterApiSub(api_client)

    def chat(self, character_id, messages):
        chat_param = ChatReqParams(
            bot_profile=CharacterKey(character_id=character_id),
            messages=messages,
            user_profile=UserProfile(user_id=str(uuid.uuid4())),
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

    def detail(self, character_id):
        self.character = self.character_api.character_details(
            character_id=character_id
        )
        self.character_name = self.character.data.name
        self.character_avatar_url = "http:" + self.character.data.avatar.file_url

    def characters(self) -> pd.DataFrame:
        body = CharacterQueryDTO(
        	where=CharacterQueryWhere(
        		scope="my" # "my", "public", "pro_configured"
        	),
        	pageNum=1,
        	pageSize=100,
        )
        return pd.DataFrame(self.character_api.search(character_query_dto=body).data.to_dict()['list'])

def BaiChuan():
    def __init__(self):
        pass

    def chat(self, messages):
        pass

def chat(role_server, character_id, messages):
    match role_server:
        case "xingchen":
            xingchen = XingChen()
            return xingchen.chat(character_id, messages)
        case "baichuan":
            baichuan = BaiChuan(character_id)
            return baichuan.chat(messages)