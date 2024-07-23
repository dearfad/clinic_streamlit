import streamlit as st
import random
import datetime
import pandas as pd
from utils import chat, PAGE_STYLE, ADMIN, CHAPTER, User
from faker import Faker

########## PAGE SETTING #############################
st.set_page_config(
    page_title="虚拟门诊",
    page_icon="👩",
    layout="centered",
)
st.html(PAGE_STYLE)
st.subheader("👩 虚拟门诊", divider="gray")
st.caption("吉林大学中日联谊医院乳腺外科")
####################################################

########## INIT AND LOGIN PAGE #############################
if "page" not in st.session_state:
    st.session_state.faker = Faker("zh_CN")
    st.session_state.page = "login"
    st.session_state.case_index = 0


def show_login():
    name = st.text_input("姓名", "无名", key="name")
    grade = st.selectbox("年级", (range(2016, 2030, 1)), key="grade")
    major = st.selectbox("专业", ("临床医学", "放射", "口腔", "其他"))
    chapter = st.selectbox(
        "章节",
        ("breast",),
        format_func=lambda x: CHAPTER[x],
    )
    st.info(
        "作为一名乳腺外科医生，请用正常语气与门诊患者沟通，问诊完毕后请输入 **我问完了**，并回答患者提出的相关问题。",
        icon="ℹ️",
    )
    if st.button("我明白了", use_container_width=True):
        if st.session_state.name == ADMIN:
            st.session_state.page = "admin"
        else:
            st.session_state.user = User(name, grade, major)
            st.session_state.user.load_questions(chapter)
            st.session_state.page = "inquiry"
        st.rerun()


######### END OF INIT AND LOGIN PAGE #############################

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "大夫，你好"},
    ]


def show_chat():
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("医"):
                st.write(message["content"])
        if message["role"] == "assistant":
            with st.chat_message("患"):
                st.markdown(f"**{message['content']}**")

##################################################################


def show_admin():
    log = pd.read_excel("data.xlsx")
    st.write(log)
##################################################################


def show_inquiries():
    st.write(st.session_state.user.chatlog)
    st.write(st.session_state.user.chatlog['questions'][0])
    st.session_state.character_id = st.session_state.user.chatlog.loc[
        st.session_state.case_index, "id"
    ]
    col_left, col_center, col_right = st.columns([1, 3, 1])
    with col_center:
        st.caption(
            f"患者编号：**{st.session_state.case_index +
                      1} / {len(st.session_state.user.chatlog)}**"
        )
        st.image(
            "https://cdn.seovx.com/?mom=302",
            caption=st.session_state.faker.name(),
            use_column_width=True,
        )

    show_chat()
    if st.session_state.user.chatlog.loc[st.session_state.case_index, 'start_time'] == '':
        st.session_state.user.chatlog.loc[st.session_state.case_index,
                                          'start_time'] = datetime.datetime.now()

    if prompt := st.chat_input(""):
        if prompt != "我问完了":
            with st.chat_message("医"):
                st.write(prompt)
                st.session_state.messages.append(
                    {"role": "user", "content": prompt})
            with st.chat_message("患"):
                response = chat(
                    role_server="xingchen",
                    character_id=st.session_state.character_id,
                    messages=st.session_state.messages,
                )
                st.markdown(f"**{response}**")
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
        else:
            st.session_state.user.chatlog.loc[st.session_state.case_index,
                                              'conversation_end_time'] = datetime.datetime.now()
            st.session_state.user.chatlog.loc[st.session_state.case_index,
                                              'messages'] = str(st.session_state.messages)
            st.session_state.page = "explain"
            st.rerun()


def show_question():
    with st.container(border=True):
        st.markdown("**对话记录**")
        show_chat()

    case_question = st.session_state.user.chatlog.loc[
        st.session_state.case_index, "questions"
    ]
    for index, question in enumerate(case_question):
        key = "a" + str(index)
        answer = st.radio(question["question"],
                          question["answer_list"], key=key)

    if st.button("提交答案", use_container_width=True):
        st.session_state.user.chatlog.loc[st.session_state.case_index, 'end_time'] = datetime.datetime.now()

        for a in range(len(case_question)):
            k = "a" + str(a)
            case_question[a]['user_answer'] = st.session_state[k]

        st.session_state.case_index = st.session_state.case_index + 1
        if st.session_state.case_index == len(st.session_state.user.chatlog):
            st.session_state.page = "result"
        else:
            st.session_state.page = "inquiry"
            del st.session_state.messages
        st.rerun()


def save_data():
    data = pd.read_excel("data.xlsx")
    log = pd.DataFrame(
        {
            "name": st.session_state.name,
            "grade": st.session_state.grade,
            "major": st.session_state.major,
            "starttime": st.session_state.starttime,
            "endtime": st.session_state.endtime,
            "chatlog": str(st.session_state.chatlog),
            "questions": str(st.session_state.questions),
        },
        index=[0],
    )
    data = pd.concat([data, log])
    data.to_excel("data.xlsx", index=False)


def show_result():
    total = len(st.session_state.user_question)
    score = 0
    st.write(st.session_state.user_question)
    st.write(st.session_state.correct_answer)
    st.write(st.session_state.user_answer)
    for i, question in enumerate(st.session_state.user_question):
        st.write(f"问题 **{i}**: {question}")
        st.write(f"正确答案: {st.session_state.correct_answer[i]}")
        st.write(f"用户答案: {st.session_state.user_answer[i]}")
        if st.session_state.correct_answer[i] == st.session_state.user_answer[i]:
            st.markdown("结果: :green[正确]")
            score += 1
        else:
            st.write("结果: :red[错误]")
        st.divider()
    st.subheader(f"医生 {st.session_state.name}")
    st.subheader(f"正确率 {round(score/total*100)}%")
    save_data()


############################################
match st.session_state.page:
    case "login":
        show_login()
    case "admin":
        show_admin()
    case "inquiry":
        show_inquiries()
    case "explain":
        show_question()
    case "result":
        show_result()
