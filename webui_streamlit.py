import streamlit as st
import random
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

#######################################################################
st.set_page_config(
    page_title="BreastVSP",
    page_icon="👩",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

st.markdown(
    """<style>
        div[class^='block-container'] {padding-top:2rem;}
        #MainMenu {visibility: hidden;}
        .stDeployButton {visibility: hidden;}
        footer {visibility: hidden;}
    </style>""",
    unsafe_allow_html=True,
)

st.subheader("📄 病例分析", divider="rainbow")
st.caption("吉林大学中日联谊医院乳腺外科")

with st.popover("登录"):
    name = st.text_input("姓名", "无名")
    grade = st.selectbox("年级", (range(2016, 2030, 1)))
    major = st.selectbox("专业", ("临床医学", "放射", "口腔", "其他"))


st.write(f"> **{name}**，{grade}级，{major}专业")
st.write("> 作为一名乳腺外科医生，请用正常语气与患者沟通，并回答相关问题。")
st.write("> 问诊完毕请输入 **我问完了**")

#######################################################################


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


#######################################################################

if "user_id" not in st.session_state:
    st.session_state.user_id = str(random.randint(1, 1000))

if "character_index" not in st.session_state:
    st.session_state.character_index = 0

if "question" not in st.session_state:
    st.session_state.question = False

if "finished" not in st.session_state:
    st.session_state.finished = False

character_list = [
    "37d0bb98a0194eefbecdba794fb1b42c",
    "5b90fa5b76f0425aab4413efd9d3c257",
]

if not st.session_state.finished:
    character_id = character_list[st.session_state.character_index]
    character = st.session_state.character_api.character_details(
        character_id=character_id
    )
    st.session_state.patient_name = character.data.name
    st.session_state.patient_avatar = character.data.avatar
    with st.container(border=True):
        col1, col2 = st.columns([1, 3], gap="large")
        with col1:
            st.image("http:" + st.session_state.patient_avatar.file_url)
        with col2:
            st.write(f"**姓名**: {st.session_state.patient_name}")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            Message(name="医生", role="user", content="你好"),
            Message(name="患者", role="assistant", content="大夫，你好"),
        ]
        chat_param = build_chat_param(
            character_id, st.session_state.messages, st.session_state.user_id
        )

    if st.session_state.question:
        answer = st.radio(
            "根据问诊，该患者的初步诊断是：",
            ["**乳腺炎**", "**乳腺癌**", "**乳腺增生**", "**乳管内乳头状瘤**"],
        )

        if st.button("提交答案"):
            if answer == "**乳腺炎**":
                st.write("你的答案：**正确**")
            else:
                st.write("你的答案：**错误**")

            st.session_state.question = False
            st.session_state.character_index = st.session_state.character_index + 1
            if st.session_state.character_index == len(character_list):
                st.session_state.finished = True
            del st.session_state.messages
            st.rerun()
    else:
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
                        character_id,
                        st.session_state.messages,
                        st.session_state.user_id,
                    )
                    res = st.session_state.chat_api.chat(chat_param)
                    st.session_state.messages.append(
                        Message(
                            name="患者",
                            role="assistant",
                            content=res.to_dict()["data"]["choices"][0]["messages"][0][
                                "content"
                            ],
                        )
                    )
                    st.write(
                        res.to_dict()["data"]["choices"][0]["messages"][0]["content"]
                    )
            else:
                st.session_state.question = True
                st.rerun()
else:
    st.write("答题结束")
