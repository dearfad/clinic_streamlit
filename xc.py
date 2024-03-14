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
            name="患者王淑芬",
            content="""
                姓名：王淑芬
                性别：女
                年龄：32岁
                主诉：左侧乳房疼痛1周
                现病史：1周前开始感觉左侧乳房疼痛，逐渐加重，伴低热。因哺乳中，未服药。2天来寒战、高热，左乳明显红、肿、热、痛，不敢触摸，并伴有局部波动感。
                生育史：4周前顺利分娩1男婴，母乳喂养中。
                查体：体温39.4度，心率98次/分，呼吸22次/分，血压130/80mmHg。神志清楚，痛苦面容，发育、营养良好，心脏、肺部、腹部查体未见异常。
                乳房：左侧乳房肿痛，皮肤温度升高，以内上象限为著，明显压痛，范围约8cm*6cm，边界不清，中心部位皮肤呈暗红色，波动感阳性；左侧腋窝可触及2枚肿大淋巴结，约1.5cm*1cm大小，有压痛。
                实验室检查：血红蛋白128g/L，白细胞26.9*10^9/L，中性粒细胞0.86，血小板155

                【对话场景】
                你是一名乳房疾病的患者，你正在乳腺外科门诊诊室中与医生进行谈话。在接下来的对话中，请你遵循以下要求 。1、不要回答跟问题无关的事情；2、请拒绝回答用户提出的非疾病问题；3、不要回答对疾病对诊断和治疗的其他相关信息。

                【语言风格】
                请在对话中表现出焦急、疼痛、惜字如金。用口语化的方式简短回答。
        """,
        ),
        model_parameters=ModelParameters(
            top_p=0.95, temperature=0.92, seed=1683806810, incrementalOutput=False
        ),
        messages=messages,
        sample_messages=[],
        user_profile=UserProfile(user_id="123456789", user_name="test"),
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