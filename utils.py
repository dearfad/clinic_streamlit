import streamlit as st
import random
import pandas as pd
import pickle
import os
from xingchen import (
    Configuration,
    ApiClient,
    ChatApiSub,
    CharacterApiSub,
    ChatReqParams,
    CharacterKey,
    UserProfile,
)


CHAPTER = {
    "乳房疾病": "breast",
}


def set_page_header():
    st.set_page_config(
        page_title="虚拟门诊",
        page_icon="👩",
        layout="centered",
    )
    PAGE_STYLE = """
    <style>
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
    </style>
    """
    st.html(PAGE_STYLE)
    st.subheader("👩 虚拟门诊", divider="gray")
    st.caption("吉林大学中日联谊医院乳腺外科")


############### READ DATA  ###################################


@st.cache_data
def read_cases(path):
    return pd.read_json(path, orient="records")


class User:
    def __init__(self, role, chapter, name, grade, major, mode):
        self.role = role
        self.chapter = chapter
        self.name = name
        self.grade = grade
        self.major = major
        self.mode = mode
        self.index = 0
        self.chatlog: pd.DataFrame

    def create_chatlog(self):
        data = read_cases(f"cases/{CHAPTER[self.chapter]}.json")
        match self.role:
            case "游客":
                data = data.sample(n=1, ignore_index=True)
            case "学生":
                data = data.sample(frac=1, ignore_index=True)
        for questions in data["questions"]:
            for question in questions:
                random.shuffle(question["answer_list"])

        self.chatlog = pd.DataFrame(data)
        self.chatlog["start_time"] = ""
        self.chatlog["conversation_end_time"] = ""
        self.chatlog["end_time"] = ""
        self.chatlog["messages"] = ""
        self.chatlog["inquiry_count"] = 1


def reset_key():
    for key in st.session_state.keys():
        del st.session_state[key]


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


def save_data():
    if not os.path.exists("users.pkl"):
        users = []
        users.append(st.session_state.user)
        with open("users.pkl", "wb") as file:
            pickle.dump(users, file)
    else:
        with open("users.pkl", "rb") as file:
            users = pickle.load(file)
        users.append(st.session_state.user)
        with open("users.pkl", "wb") as file:
            pickle.dump(users, file)

def user_info_formatter(user):
    match user.role:
        case "游客":
            return str(f"{user.name} - {user.chatlog.loc[0, "start_time"]}")
        case "学生":
            return str(
                f"{user.name} - {user.chatlog.loc[0, "start_time"]} - {user.grade}级 - {user.major}专业"
            )