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
    Message,
    UserProfile,
)

########## PAGE SETTING ##################
st.set_page_config(
    page_title="乳腺外科虚拟门诊",
    page_icon="👩",
    layout="centered",
)

st.html(
    """<style>
        header {visibility: hidden;}
        .block-container{
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        .st-emotion-cache-arzcut{
            padding-bottom: 1rem;
        }
    </style>"""
)

########## END OF PAGE SETTING ##########

st.subheader("📄 虚拟门诊", divider="gray")
st.caption("吉林大学中日联谊医院乳腺外科")


########## XINGCHEN CONFIG ##################
configuration = Configuration(host="https://nlp.aliyuncs.com")
configuration.access_token = "lm-bw72h4Q9oFOyuE47ncPxbg=="
with ApiClient(configuration) as api_client:
    st.session_state.chat_api = ChatApiSub(api_client)
    st.session_state.character_api = CharacterApiSub(api_client)


def build_chat_param(character_id, messages, user_id):
    return ChatReqParams(
        bot_profile=CharacterKey(character_id=character_id),
        messages=messages,
        user_profile=UserProfile(user_id=user_id),
    )


########## END OF XINGCHEN CONFIG ##########

########## CASES ###########################

if "cases" not in st.session_state:
    st.session_state.cases = pd.read_excel("cases.xlsx", index_col='id')

if "character_list" not in st.session_state:
    st.session_state.character_list = [
        "37d0bb98a0194eefbecdba794fb1b42c",
        "5b90fa5b76f0425aab4413efd9d3c257",
        "de2f24bd946e4c3fa80047d6877f557b"
    ]
    random.shuffle(st.session_state.character_list)
############################################

######### INIT #############################
if "user_id" not in st.session_state:
    st.session_state.user_id = str(random.randint(1, 1000))

if "character_index" not in st.session_state:
    st.session_state.character_index = 0

if "messages" not in st.session_state:
    st.session_state.messages = [
        Message(name="医生", role="user", content="你好"),
        Message(name="患者", role="assistant", content="大夫，你好"),
    ]

if "page" not in st.session_state:
    st.session_state.page = "login"
    st.session_state.name = ""
    st.session_state.grade = ""
    st.session_state.major = ""

if "user_question" not in st.session_state:
    st.session_state.user_question = []
    st.session_state.user_answer = []
    st.session_state.correct_answer = []

if "answering" not in st.session_state:
    st.session_state.answering = False
###########################################
def make_inquiries():
    st.session_state.character_id = st.session_state.character_list[st.session_state.character_index]
    character = st.session_state.character_api.character_details(
        character_id=st.session_state.character_id
    )
    st.session_state.patient_name = character.data.name
    st.session_state.patient_avatar = character.data.avatar
    st.image(
        "http:" + st.session_state.patient_avatar.file_url,
        caption=st.session_state.patient_name,
    )
    chat_param = build_chat_param(
        st.session_state.character_id, st.session_state.messages, st.session_state.user_id
    )

    for message in st.session_state.messages:
        if message.role == "user":
            with st.chat_message("医"):
                st.write(message.content)
        if message.role == "assistant":
            with st.chat_message("患"):
                st.write(message.content)

    if prompt := st.chat_input(""):
        if prompt != "我问完了":
            with st.chat_message("医"):
                st.write(prompt)
            st.session_state.messages.append(
                Message(name="医生", role="user", content=prompt)
            )
            with st.chat_message("患"):
                chat_param = build_chat_param(
                    st.session_state.character_id,
                    st.session_state.messages,
                    st.session_state.user_id,
                )
                response = st.session_state.chat_api.chat(chat_param)
                st.session_state.messages.append(
                    Message(
                        name="患者",
                        role="assistant",
                        content=response.to_dict()["data"]["choices"][0]["messages"][0][
                            "content"
                        ],
                    )
                )
                st.write(
                    response.to_dict()["data"]["choices"][0]["messages"][0]["content"]
                )
        else:
            st.session_state.page = "explain"
            st.rerun()


def make_explain():

        case_question = st.session_state.cases.loc[st.session_state.character_id, 'question'].split('?')
        case_answer = st.session_state.cases.loc[st.session_state.character_id, 'answer'].split(';')
        for index, question in enumerate(case_question):
            if not st.session_state.answering:
                st.session_state.user_question.append(question)
            answer_list = []
            for answer in case_answer[index].split(','):
                answer_list.append(answer)
            if not st.session_state.answering:
                st.session_state.correct_answer.append(answer_list[0])

            key = 'a'+str(index)
            answer = st.radio(
                question,
                answer_list,
                key=key
            )
        if not st.session_state.answering:
            st.session_state.answering = True
        st.write(st.session_state.user_question)

        if st.button("提交答案"):


            for a in range(len(case_question)):
                k = 'a' + str(a)
                st.session_state.user_answer.append(st.session_state[k])




            st.session_state.character_index = st.session_state.character_index + 1
            if st.session_state.character_index == len(st.session_state.character_list):
                st.session_state.page = "result"
                if st.button('结束', type="primary", use_container_width=True):
                    st.rerun()
            else:
                st.session_state.page = "inquiry"
                st.session_state.answering = False
                del st.session_state.messages
                if st.button('下一位患者', use_container_width=True):
                    st.rerun()


############################################
match st.session_state.page:
    case "login":
        st.session_state.name = st.text_input("姓名", "无名")
        st.session_state.grade = st.selectbox("年级", (range(2016, 2030, 1)))
        st.session_state.major = st.selectbox(
            "专业", ("临床医学", "放射", "口腔", "其他")
        )
        st.info(
            "作为一名乳腺外科医生，请用正常语气与门诊患者沟通，问诊完毕后请输入 **我问完了**，并回答患者提出的相关问题。",
            icon="ℹ️",
        )
        if st.button("我明白了", use_container_width=True):
            st.session_state.page = "inquiry"
            st.rerun()
    case "inquiry":
        st.write("医生：", st.session_state.name)
        make_inquiries()
    case "explain":
        st.write("explain")
        make_explain()
    case "result":
        st.write("result")
        st.write(st.session_state.user_question)
        st.write(st.session_state.correct_answer)
        st.write(st.session_state.user_answer)
