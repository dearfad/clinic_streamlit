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
    menu_items=None
)

st.title('乳房疾病病例分析')

if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    login_placeholder = st.empty()
    with login_placeholder.container():
        with st.form('login_form'):
            st.session_state.name = st.text_input('姓名', value='无名氏')
            st.session_state.grade = st.selectbox('年级',tuple(range(2010,2030)))
            login_bt = st.form_submit_button('登录', use_container_width=True)

    if login_bt:
        if st.session_state.name:
            login_placeholder.empty()
            st.session_state.login = True
        else:
            st.error('请输入姓名', icon="🚨")
if st.session_state.login:
    st.divider()
    st.write(f"**医生：** {st.session_state.name}， **年级：** {st.session_state.grade}")
    st.session_state.patient='赵淑娟'
    st.session_state.id = 1
    st.write('**地点：** 乳腺外科门诊')
    st.write('请输入你的问诊话语，结束请输入**我问完了**')
    st.divider()
    st.write(f"**患者姓名：** {st.session_state.patient}， **就诊编号：** {st.session_state.id}")

system_msg = """
你是一名乳房疾病的患者，现在你正在乳腺外科门诊诊室和医生谈话。下面是你的特征：女,32岁。左乳房红肿,疼痛1周,伴发热2天。1周前开始感觉左乳房疼痛,逐渐加重,伴低热,因哺乳中,未服药,2天来寒战、高热,左乳明显红、肿、热、痛,不敢触摸,并伴有局部波动感,4周前顺利分娩1男婴,母乳喂养。
查体:T39.4℃,P98次/分,R22次/分,BP130/80mmHg,神志清楚,痛苦面容,发育、营养良好,心肺、腹查体未见异常,外科情况:左乳房肿痛,发热,以内上方为主,明显压痛,范围约8cm*6cm,边界不清,中心部位呈暗红色,波动感阳性,左侧腋窝可触及2枚肿大淋巴结,约1.5cm*1cm大小,有压痛。
实验室检查:血常规128g/L,WBC26.9*109/L,N0.86,PLT155*109/L。
在接下来的对话中,请遵循以下要求:1.请回答用户的提出的疾病相关的问题。2.请拒绝回答用户提出的非疾病问题。3、不要回答对疾病对诊断和治疗的问题。
"""


if "messages" not in st.session_state:
    st.session_state.messages = [{'role': 'system', 'content': system_msg},{'role':'user', 'content': '哪里不舒服'},{'role':'assistant', 'content': '乳房不舒服'}]

if not st.session_state.messages:
    st.session_state.messages = [{'role': 'system', 'content': system_msg},{'role':'user', 'content': '哪里不舒服'},{'role':'assistant', 'content': '乳房不舒服'}]

if st.session_state.login:
    for message in st.session_state.messages:
        if message['role'] != 'system':
            if message['role']=='user':
                with st.chat_message('医'):
                    st.text(message["content"])
            if message['role']=='assistant':
                with st.chat_message('患'):
                    st.text(message["content"])       

prompt = st.chat_input("")

if prompt:
    with st.chat_message('医'):
        st.text(prompt)

    st.session_state.messages.append({'role': 'user', 'content': prompt})


    with st.chat_message('患'):
        response = Generation.call(
            'qwen-1.8b-chat',
            messages=st.session_state.messages,
            # set the random seed, optional, default to 1234 if not set
            seed=random.randint(1, 10000),
            result_format='message',  # set the result to be "message"  format.
        )
        if response.status_code == HTTPStatus.OK:
            response_placeholder = st.empty()
            response_placeholder.text(response.output.choices[0]['message']['content'])
            
        st.session_state.messages.append({'role': response.output.choices[0]['message']['role'],'content': response.output.choices[0]['message']['content']})