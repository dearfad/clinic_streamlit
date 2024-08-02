import streamlit as st
import random
import pandas as pd
import pickle
import os
from datetime import datetime
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

INIT_CONVERSATION = [
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "大夫，你好"},
]

ADMIN = "DEARFAD"

CHAPTER = {
    'breast': '乳房疾病',
}

############### READ DATA  ###################################


@st.cache_data
def read_cases(path):
    return pd.read_json(path, orient="records")


def get_qa(chapter, num, seq):
    data = read_cases(f"cases/{chapter}.json")
    if num == 'all' and seq == 'random':
        return data.sample(frac=1, ignore_index=True)


CHATLOG_COLUMNS = ['id', 'server', 'name', 'questions',
                   'start_time', 'conversation_end_time', 'end_time', 'messages', 'inquiry_count']


class User:
    def __init__(self, role, chapter, name, grade, major):
        self.role = role
        self.chapter = chapter
        self.name = name
        self.grade = grade
        self.major = major
        self.chatlog = pd.DataFrame(columns=CHATLOG_COLUMNS)

    def load_patients(self, num='all', seq='random'):
        self.chatlog = get_qa(chapter, num, seq)
        self.chatlog['start_time'] = ''
        self.chatlog['conversation_end_time'] = ''
        self.chatlog['end_time'] = ''
        self.chatlog['messages'] = ''
        self.chatlog['inquiry_count'] = 1


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

    def chat(self, messages):
        chat_param = ChatReqParams(
            bot_profile=CharacterKey(character_id=self.character_id),
            messages=messages,
            user_profile=UserProfile(user_id=self.user_id),
        )
        try:
            response = self.chat_api.chat(chat_param).to_dict()
            if response['success']:
                return response["data"]["choices"][0]["messages"][0]["content"]
            else:
                return f"( 似乎自己在思索什么，嘴里反复说着数字 ~ {response['code']} ~ )"
        except:
            return f"( 脑子坏掉了，等会再问我吧 ~ )"

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


def save_data():
    if not os.path.exists('users.pkl'):
        users = []
        users.append(st.session_state.user)
        with open('users.pkl', 'wb') as file:
            pickle.dump(users, file)
    else:
        with open('users.pkl', 'rb') as file:
            users = pickle.load(file)
        users.append(st.session_state.user)
        with open('users.pkl', 'wb') as file:
            pickle.dump(users, file)
