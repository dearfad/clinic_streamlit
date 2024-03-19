import streamlit as st
import random
from http import HTTPStatus
from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role

st.set_page_config(
    page_title="BreastVSP",
    page_icon="👩",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

st.title("乳房疾病病例分析")
st.caption("吉林大学中日联谊医院乳腺外科")

patient_info = """
【性别】女
【年龄】32岁
【主诉】左侧乳房红肿、疼痛1周，伴发热2天。
【现病史】1周前开始感觉左乳房疼痛,逐渐加重,伴低热,因哺乳中,未服药,2天来寒战、高热,左乳明显红、肿、热、痛,不敢触摸,并伴有局部波动感,4周前顺利分娩1男婴,母乳喂养。
【查体】
体温 39.4度
心率 98次/分
呼吸 22次/分
血压 130/80mmHg
神志清楚,痛苦面容,发育、营养良好,心肺、腹查体未见异常
【外科情况】左侧乳房肿痛,发热,以内上象限为主,明显压痛,范围约8cm*6cm,边界不清,中心部位呈暗红色,波动感阳性,左侧腋窝可触及2枚肿大淋巴结,约1.5cm*1cm大小,有压痛。
【实验室检查】血常规128g/L,WBC26.9*10^9/L,N0.86,PLT155*10^9/L。
"""

system_msg = """
你是一名乳房疾病的患者，现在你正在乳腺外科门诊诊室和医生谈话。
在接下来的对话中,请遵循以下要求:
0. 不要回答个人信息里面没有的内容
1. 请根据你的个人信息回答用户的提出的疾病相关的问题
2. 请拒绝回答用户提出的非疾病问题
3. 不要回答对疾病对诊断和治疗的问题
4. 当你对问题不够确定时，你要坦诚地说出来。面对不明确或有歧义的问题时，你要进一步询问以便明白我的需求
你的个人信息：{patient_info}
"""


if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "医生，你好"},
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        if message["role"] == "user":
            with st.chat_message("医"):
                st.write(message["content"])
        if message["role"] == "assistant":
            with st.chat_message("患"):
                st.write(message["content"])

prompt = st.chat_input("")

if prompt:
    with st.chat_message("医"):
        st.write(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("患"):
        response = Generation.call(
            "qwen-1.8b-chat",
            # "baichuan-7b-v1",
            messages=st.session_state.messages,
            # set the random seed, optional, default to 1234 if not set
            # seed=random.randint(1, 10000),
            result_format="message",  # set the result to be "message"  format.
        )
        if response.status_code == HTTPStatus.OK:
            response_placeholder = st.empty()
            response_placeholder.write(response.output.choices[0]["message"]["content"])

        st.session_state.messages.append(
            {
                "role": response.output.choices[0]["message"]["role"],
                "content": response.output.choices[0]["message"]["content"],
            }
        )
