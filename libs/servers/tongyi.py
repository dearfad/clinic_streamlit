import random

import pandas as pd
import streamlit as st
from xingchen import (
    ApiClient,
    CharacterApiSub,
    CharacterKey,
    CharacterQueryDTO,
    CharacterQueryWhere,
    CharacterUpdateDTO,
    ChatApiSub,
    ChatContext,
    ChatReqParams,
    ChatMessageApiSub,
    ChatHistoryQueryDTO,
    ChatHistoryQueryWhere,
    ResetChatHistoryRequest,
    Configuration,
    Message,
    ModelParameters,
    UserProfile,
)


class XingChen:
    def __init__(self):
        self.configuration = Configuration(host="https://nlp.aliyuncs.com")
        # xingchen QPS=1 APIMAX=10
        self.configuration.access_token = random.choice(st.secrets["xingchen_api_keys"])
        with ApiClient(self.configuration) as api_client:
            self.chat_api = ChatApiSub(api_client)
            self.character_api = CharacterApiSub(api_client)
            self.chat_message_api = ChatMessageApiSub(api_client)

    def chat(self, character_id, message, user_id) -> str:
        chat_param = ChatReqParams(
            bot_profile=CharacterKey(character_id=character_id),
            model_parameters=ModelParameters(
                seed=random.getrandbits(32), incrementalOutput=False
            ),
            messages=[Message(role="user", content=message)],
            context=ChatContext(use_chat_history=True),
            user_profile=UserProfile(user_id=user_id),
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

    def character_create():
        pass

    def character_delete(self, character_id):
        pass

    def character_update(self, character):
        body = CharacterUpdateDTO.from_dict(character)
        st.write(body)
        result = self.character_api.update(character_update_dto=body)
        # result = self.character_api.update(character_update_dto=body).to_dict()['success']
        return result

    def character_details(self, character_id) -> dict:
        detail = self.character_api.character_details(character_id=character_id)
        return detail.data.to_dict()

    def character_search(self, scope="my") -> list:
        body = CharacterQueryDTO(
            where=CharacterQueryWhere(
                scope=scope  # "my", "public", "pro_configured"
            ),
            pageNum=1,
            pageSize=100,
        )
        result = self.character_api.search(character_query_dto=body)
        return result.data.to_dict()["list"]

    def get_chat_histories(self, character_id, user_id, session_id) -> list:
        body = ChatHistoryQueryDTO(
            where=ChatHistoryQueryWhere(
                characterId=character_id, bizUserId=user_id, sessionId=session_id
            ),
            orderBy=["gmtCreate asc"],
            pageNum=1,
            pageSize=100,
        )
        result = self.chat_message_api.chat_histories(chat_history_query_dto=body)
        return result.data.to_dict()

    def reset_chat_history(self, character_id, user_id) -> bool:
        body = ResetChatHistoryRequest(characterId=character_id, userId=user_id)
        result = self.chat_message_api.reset_chat_history(request=body)
        return result.data


model = XingChen()

if st.button("test"):

    character = model.character_details("5b90fa5b76f0425aab4413efd9d3c257")
    st.write(plugins)
    result = model.character_update(character)
    st.write(result)

s = """
姓名：赵淑芹
性别：女
年龄：20岁
主诉：右侧乳房肿物3天
现病史：3天前突然发现左侧乳房肿块，无疼痛，未予治疗。
生育史：未婚，未育。
查体：体温36.0度，心率80次/分，呼吸20次/分，血压120/80mmHg。神志清楚，发育、营养良好，心脏、肺部、腹部查体未见异常。
乳房：右侧乳房外上象限可以触及2*2厘米肿物，边界清楚，质地硬，活动度良好，无压痛，皮肤颜色正常
抽血化验：血常规检查正常
超声检查：未做

【对话场景】
你是一名乳房疾病的患者，你正在乳腺外科门诊诊室中与医生进行谈话。在接下来的对话中，请你遵循以下要求 。1、不要回答跟问题无关的事情；2、请拒绝回答用户提出的非疾病问题；3、不要回答对疾病对诊断和治疗的其他相关信息。4、不能说出你的姓名。

【语言风格】
请在对话中表现出焦急、疼痛、惜字如金。用口语化的方式简短回答。
聊天开场白大夫，你好
强制要求
对话示例
"""
