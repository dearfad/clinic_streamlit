import streamlit as st
from xingchen import (
    Configuration,
    ApiClient,
    ChatApiSub,
    ChatReqParams,
    CharacterKey,
    Message,
    UserProfile,
    ModelParameters,
)

st.set_page_config(
    page_title="BreastVSP",
    page_icon="👩",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

st.title("乳房疾病病例分析")
st.caption("吉林大学中日联谊医院乳腺外科")
st.write('**你是一名乳腺外科医生，现在用平常谈话的方法跟眼前的患者沟通，请尝试做出你的诊断。**')


def build_chat_param(messages):
    return ChatReqParams(
        bot_profile=CharacterKey(
            character_id="37d0bb98a0194eefbecdba794fb1b42c",
            version=1
        ),
        model_parameters=ModelParameters(
            top_p=0.95, temperature=0.92, seed=1683806810, incrementalOutput=False
        ),
        messages=messages,
        sample_messages=[],
        user_profile=UserProfile(user_id="123456789", user_name="doctor"),
    )


if "messages" not in st.session_state:
    configuration = Configuration(host="https://nlp.aliyuncs.com")
    configuration.access_token = "lm-bw72h4Q9oFOyuE47ncPxbg=="
    with ApiClient(configuration) as api_client:
        st.session_state.api = ChatApiSub(api_client)
    st.session_state.messages = [
        Message(name='医生', role="user", content="你好"),
        Message(name='患者', role="assistant", content="大夫，你好"),
        Message(name='医生', role="user", content="哪里不舒服？"),
    ]
    chat_param = build_chat_param(st.session_state.messages)
    res = st.session_state.api.chat(chat_param)
    st.session_state.messages.append(Message(name='患者', role='assistant', content=res.to_dict()["data"]["choices"][0]["messages"][0]["content"]))

for message in st.session_state.messages:
    if message.role == "user":
        with st.chat_message("医"):
            st.write(message.content)
    if message.role == "assistant":
        with st.chat_message("患"):
            st.write(message.content)


prompt = st.chat_input("")

if prompt:
    with st.chat_message("医"):
        st.write(prompt)

    st.session_state.messages.append(Message(name='医生', role="user", content=prompt))
    
    with st.chat_message("患"):
        chat_param = build_chat_param(st.session_state.messages)
        res = st.session_state.api.chat(chat_param)
        st.session_state.messages.append(Message(name='患者', role='assistant', content=res.to_dict()["data"]["choices"][0]["messages"][0]["content"]))
        response_placeholder = st.empty()
        response_placeholder.write(res.to_dict()["data"]["choices"][0]["messages"][0]["content"])