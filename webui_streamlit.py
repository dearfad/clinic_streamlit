import streamlit as st
from datetime import datetime
from utils import chat, PAGE_STYLE, ADMIN, CHAPTER, INIT_CONVERSATION, User, save_data
from faker import Faker
import pickle

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
    st.session_state.page = "login"
    st.session_state.faker = Faker("zh_CN")
    st.session_state.case_index = 0

if "messages" not in st.session_state:
    st.session_state.messages = INIT_CONVERSATION


def show_login():
    role = st.selectbox("**类别**", ('游客', '学生', '教师', '管理员'))
    match role:
        case "游客":
            chapter = st.selectbox(
                "**章节**",
                ("breast",),
                format_func=lambda x: CHAPTER[x],
            )
            st.info("请用**正常语气**与随机一名患者沟通", icon=":material/counter_1:")
            st.info("问诊完毕后请输入 **我问完了**", icon=":material/counter_2:")
            st.info("回答患者提出的**相关问题**", icon=":material/counter_3:")
            st.info("**重新开始**请按 **F5** 或 :material/refresh: 页面",
                    icon=":material/counter_4:")
            st.info("作为一名**游客**，您的过程不被统计", icon=":material/counter_5:")
            if st.button('开始', use_container_width=True):
                st.session_state.user = User(
                    role=role, chapter=chapter, name='游客', grade='', major='')
                # st.session_state.user.load_patients(chapter)
                st.session_state.page = 'inquiry'
                st.rerun()
        case '学生':
            chapter = st.selectbox(
                "**章节**",
                ("breast",),
                format_func=lambda x: CHAPTER[x],
            )
            name = st.text_input("**姓名**", "学生")
            grade = st.selectbox("**年级**", (range(2016, 2030, 1)))
            major = st.selectbox("**专业**", ("临床医学", "放射", "口腔", "其他"))

            if st.button('开始', use_container_width=True):
                st.session_state.user = User(role, chapter, name, grade, major)
                st.session_state.user.load_patients(chapter)
                st.session_state.page = "inquiry"
                st.rerun()
        case '教师':
            pass
        case '管理员':
            password = st.text_input("**密码**")
            if st.button('登录', use_container_width=True):
                if password == ADMIN:
                    st.session_state.page = 'admin'
                    st.rerun()
                else:
                    st.warning(":material/key: **密码错误**，请咨询**管理员**相关信息")

    # if st.button("我明白了", use_container_width=True):
    #     if st.session_state.name == ADMIN:
    #         st.session_state.page = "admin"
    #     else:
    #         st.session_state.user = User(name, grade, major)
    #         st.session_state.user.load_questions(chapter)
    #         st.session_state.page = "inquiry"
    #     st.rerun()


######### END OF INIT AND LOGIN PAGE #############################


def show_chat():
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("医"):
                st.write(message["content"])
        if message["role"] == "assistant":
            with st.chat_message("患"):
                st.markdown(f"**{message['content']}**")

##################################################################


##################################################################

def show_inquiries():
    st.write(st.session_state.user.chatlog)
    st.session_state.character_id = st.session_state.user.chatlog.loc[
        st.session_state.case_index, "id"
    ]
    col_left, col_center, col_right = st.columns([1, 3, 1])
    with col_center:
        st.caption(
            f"患者编号：**{st.session_state.case_index+1} / {len(st.session_state.user.chatlog)}**")
        st.image(
            "https://cdn.seovx.com/d/?mom=302",
            caption=st.session_state.faker.name(),
            use_column_width=True,
        )

    show_chat()
    if st.session_state.user.chatlog.loc[st.session_state.case_index, 'start_time'] == '':
        st.session_state.user.chatlog.loc[st.session_state.case_index,
                                          'start_time'] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

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
                                              'conversation_end_time'] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            st.session_state.messages.append(
                {"role": "user", "content": prompt})
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

    if st.button('再问一下', use_container_width=True):
        st.session_state.page = 'inquiry'
        st.session_state.user.chatlog.loc[st.session_state.case_index,
                                          'inquiry_count'] += 1
        st.rerun()

    if st.button("提交答案", use_container_width=True):
        st.session_state.user.chatlog.loc[st.session_state.case_index,
                                          'end_time'] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        for a in range(len(case_question)):
            k = "a" + str(a)
            case_question[a]['user_answer'] = st.session_state[k]

        st.session_state.case_index = st.session_state.case_index + 1
        if st.session_state.case_index == len(st.session_state.user.chatlog):
            save_data()
            st.session_state.page = "result"
        else:
            st.session_state.page = "inquiry"
            del st.session_state.messages
        st.rerun()


def show_result(user: User) -> None:

    with st.container(border=True):
        col_name, col_grade, col_major = st.columns(3)
        with col_name:
            st.markdown(f"**姓名: {user.name}**")
        with col_grade:
            st.markdown(f"年级: {user.grade}")
        with col_major:
            st.markdown(f"专业: {user.major}")

        user_start_time = datetime.strptime(
            user.chatlog.loc[0, 'start_time'], "%Y/%m/%d %H:%M:%S")
        user_end_time = datetime.strptime(user.chatlog.loc[len(
            user.chatlog['questions'])-1, 'end_time'], "%Y/%m/%d %H:%M:%S")
        st.markdown(f":date: {user.chatlog.loc[0, 'start_time']}")
        st.markdown(f":stopwatch: {user_end_time-user_start_time}")

    score = 0
    total_questions_count = 0
    normal_inquiry_count = len(user.chatlog['questions'])
    total_inquiry_count = 0

    for i, question in enumerate(user.chatlog['questions']):
        st.divider()
        start_time = datetime.strptime(
            user.chatlog.loc[i, 'start_time'], "%Y/%m/%d %H:%M:%S")
        conversation_end_time = datetime.strptime(
            user.chatlog.loc[i, 'conversation_end_time'], "%Y/%m/%d %H:%M:%S")
        end_time = datetime.strptime(
            user.chatlog.loc[i, 'end_time'], "%Y/%m/%d %H:%M:%S")
        col_question_left, col_question_right = st.columns(2)
        with col_question_left:
            st.markdown(
                f"**:ok_woman: {i+1}/{len(user.chatlog['questions'])}**")
        with col_question_right:
            st.markdown(
                f"**:stopwatch: {end_time-start_time} = {conversation_end_time-start_time} + {end_time-conversation_end_time}**")
        with st.container(border=True):
            st.markdown(f"**对话记录**")
            st.markdown(f"**:repeat: {user.chatlog.loc[i, 'inquiry_count']}**")
            total_inquiry_count += user.chatlog.loc[i, 'inquiry_count']
            st.session_state.messages = eval(user.chatlog.loc[i, 'messages'])
            show_chat()
        for q in question:
            total_questions_count += 1
            st.markdown(f"**Q{total_questions_count}: {q['question']}**")
            st.markdown(f"答案选项: 🔹{' 🔹'.join(q['answer_list'])}")
            st.markdown(f"正确答案: :white_check_mark:**{q['correct_answer']}**")
            if q['correct_answer'] == q['user_answer']:
                score += 1
                st.markdown(f"用户回答: :white_check_mark:**{q['user_answer']}**")
            else:
                st.markdown(f"用户回答: :x:**:red[{q['user_answer']}]**")
    st.divider()
    question_score = round(score/total_questions_count*100)
    inquiry_score = (total_inquiry_count-normal_inquiry_count)*2
    st.markdown(f"**问题得分: {score} :material/pen_size_2: {
                total_questions_count} :material/close:100 :material/equal: {question_score}**")
    st.markdown(f"**复问扣分: ( {total_inquiry_count} - {
                normal_inquiry_count} ) :material/close:2 :material/equal: {inquiry_score}**")
    st.markdown(f"**最后得分: :small_orange_diamond: :red[{
                question_score - inquiry_score}] :small_orange_diamond:**")


def show_admin():
    with open('users.pkl', 'rb') as file:
        users = pickle.load(file)

    user = st.selectbox('**用户**', users, format_func=lambda x: str(
        f"{x.name} - {x.grade}级 - {x.major}专业"),)
    show_result(user)


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
        show_result(st.session_state.user)
