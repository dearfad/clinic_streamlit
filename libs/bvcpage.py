import streamlit as st
from datetime import datetime
from libs.bvcutils import read_info
from libs.servers.tongyi import XingChen


def set_page_header():
    st.set_page_config(
        page_title="虚拟门诊",
        page_icon="👩",
        layout="centered",
    )
    PAGE_STYLE = """
    <style>
        header{
            visibility: hidden;
        }
        audio{
            display: none;
        }
        img{
            border-radius: 50%;
            border: 1px solid #ddd;
            padding: 5px;
        }
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


def show_chat(messages):
    for message in messages:
        if message["role"] == "user":
            with st.chat_message("医"):
                st.write(message["content"])
        if message["role"] == "assistant":
            with st.chat_message("患"):
                st.markdown(f"**{message['content']}**")


def show_patient_info(character_id):
    info_df = read_info("cases/breast_info.json").set_index("id")
    info = info_df.loc[character_id, "info"]
    st.markdown(":book: **患者信息**")
    for key, value in info.items():
        st.markdown(f"**{key}：** {value}")


def show_result(user):
    with st.container(border=True):
        col_name, col_grade, col_major = st.columns(3)
        with col_name:
            st.markdown(f"**姓名: {user.name}**")
        with col_grade:
            st.markdown(f"年级: {user.grade}")
        with col_major:
            st.markdown(f"专业: {user.major}")
        user_start_time = datetime.strptime(
            user.chatlog.loc[0, "start_time"], "%Y-%m-%d %H:%M:%S"
        )
        user_end_time = datetime.strptime(
            user.chatlog.loc[len(user.chatlog["questions"]) - 1, "end_time"],
            "%Y-%m-%d %H:%M:%S",
        )
        st.markdown(f":date: {user.chatlog.loc[0, 'start_time']}")
        st.markdown(f":stopwatch: {user_end_time-user_start_time}")

    score = 0
    total_questions_count = 0
    normal_inquiry_count = len(user.chatlog["questions"])
    total_inquiry_count = 0

    for i, question in enumerate(user.chatlog["questions"]):
        st.divider()
        start_time = datetime.strptime(
            user.chatlog.loc[i, "start_time"], "%Y-%m-%d %H:%M:%S"
        )
        conversation_end_time = datetime.strptime(
            user.chatlog.loc[i, "conversation_end_time"], "%Y-%m-%d %H:%M:%S"
        )
        end_time = datetime.strptime(
            user.chatlog.loc[i, "end_time"], "%Y-%m-%d %H:%M:%S"
        )
        col_question_left, col_question_right = st.columns(2)
        with col_question_left:
            st.markdown(f"**:ok_woman: {i+1}/{len(user.chatlog['questions'])}**")
        with col_question_right:
            st.markdown(
                f"**:stopwatch: {end_time-start_time} = {conversation_end_time-start_time} + {end_time-conversation_end_time}**"
            )

        with st.container(border=True):
            character_id = user.chatlog.loc[i, "id"]
            show_patient_info(character_id)

        with st.container(border=True):
            st.markdown(":clipboard: **对话记录**")
            st.markdown(f"**:repeat: {user.chatlog.loc[i, 'inquiry_count']}**")
            total_inquiry_count += user.chatlog.loc[i, "inquiry_count"]
            show_chat(eval(user.chatlog.loc[i, "messages"]))
        for q in question:
            total_questions_count += 1
            st.markdown(f"**Q{total_questions_count}: {q['question']}**")
            st.markdown(f"答案选项: 🔹{' 🔹'.join(q['answer_list'])}")
            st.markdown(f"正确答案: :white_check_mark:**{q['correct_answer']}**")
            if q["correct_answer"] == q["user_answer"]:
                score += 1
                st.markdown(f"用户回答: :white_check_mark:**{q['user_answer']}**")
            else:
                st.markdown(f"用户回答: :x:**:red[{q['user_answer']}]**")

    st.divider()

    question_score = round(score / total_questions_count * 100)
    inquiry_score = (total_inquiry_count - normal_inquiry_count) * 2
    st.markdown(f"**问题得分: {score} :material/pen_size_2: {
                total_questions_count} :material/close:100 :material/equal: {question_score}**")
    st.markdown(f"**复问扣分: ( {total_inquiry_count} - {
                normal_inquiry_count} ) :material/close:2 :material/equal: {inquiry_score}**")
    st.markdown(f"**最后得分: :small_orange_diamond: :red[{
                question_score - inquiry_score}] :small_orange_diamond:**")


def show_character_info(character):
    with st.container(border=False):
        col_left, col_right = st.columns([1, 3])
        with col_right:
            with st.container(border=True):
                st.markdown(f"姓名: **{character['name']}**")
                st.markdown(f"建立: **{str(character['gmtCreate']).split(' ')[0]}**")
                st.markdown(f"更新: **{str(character['gmtModified']).split(' ')[0]}**")
                basicinfo = st.text_area(
                    label="**基本信息**",
                    height=500,
                    value=character["basicInformation"],
                )
        with col_left:
            avatar_url = "http:" + character["avatar"]["fileUrl"]
            st.image(avatar_url, caption=character["name"], use_column_width=True)

            if st.button("**刷新**", use_container_width=True):
                st.rerun()
            if st.button("**更新**", use_container_width=True):
                character["basicInformation"] = basicinfo
                xingchen = XingChen()
                result = xingchen.update(character)
                if result:
                    st.markdown("**:green[成功...]**")
                else:
                    st.markdown("**:red[失败...]**")
