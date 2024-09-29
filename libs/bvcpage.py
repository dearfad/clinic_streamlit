import streamlit as st


from libs.bvcclasses import Role, User
from libs.bvcutils import read_patients, reset_session_state, get_current_user

from streamlit_cookies_controller import CookieController, RemoveEmptyElementContainer

@st.cache_data
def get_controller():
    return CookieController()

def set_page_header(layout="centered"):
    st.set_page_config(
        page_title="虚拟门诊",
        page_icon=":health_worker:",
        layout=layout,
        initial_sidebar_state='auto',
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
            border-radius: 8px;
            border: 1px solid #ddd;
            padding: 5px;
            width: 100%;
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
        div[data-testid='element-container']:has(iframe[title='streamlit_cookies_controller.cookie_controller.cookie_controller']){
            display:none;
        }
    </style>
    """
    st.html(PAGE_STYLE)
    st.session_state.cookiecontroller = get_controller()
    with st.empty():
        get_current_user(st.session_state.cookiecontroller)
    col_title, col_user = st.columns(2)
    with col_title:
        st.markdown(":heavy_minus_sign: **虚拟门诊** :heavy_minus_sign:")
    with col_user:
        st.markdown(f":id: **{st.session_state.user}**")

def set_current_user(cookiecontroller, name):
    print(cookiecontroller)
    cookiecontroller.set("user", name)
    st.session_state.user = name

def set_page_footer():
    col_footer_left, col_footer_center, col_footer_right = st.columns(3)
    with col_footer_left:
        if st.button("RERUN", use_container_width=True):
            st.rerun()
    with col_footer_center:
        if st.button("退出登录", use_container_width=True, type="primary"):
            set_current_user(st.session_state.cookiecontroller, name="游客")
            st.switch_page("clinic.py")
    with col_footer_right:
        if st.button("返回首页", use_container_width=True):
            st.switch_page("clinic.py")


def show_setting_page():
    col_left, col_center, col_right = st.columns(3)
    with col_left:
        if st.button("返回首页"):
            reset_session_state()
            st.switch_page("clinic.py")
    with col_right:
        if "voice" not in st.session_state:
            st.session_state.voice = False
        setting_popover = st.popover(":material/settings:**设置**")
        with setting_popover:
            voice = st.toggle("**语音输出**", value=st.session_state.voice)
            st.session_state.voice = True if voice else False
    if "doctor" not in st.session_state:
        st.warning("**用户信息丢失，请点击返回首页**")
        st.stop()


def show_role_info(role):
    match role:
        case Role.VISITOR:
            st.info(
                "请用 **正常语气** 与 **随机一名患者** 沟通",
                icon=":material/counter_1:",
            )
            st.info("问诊完毕后请输入 **我问完了**", icon=":material/counter_2:")
            st.info("回答患者提出的 **相关问题**", icon=":material/counter_3:")
            st.info(
                "作为一名 **游客**，您的过程 **不被统计**", icon=":material/counter_4:"
            )

        case Role.STUDENT:
            st.info(
                "请用 **正常语气** 与 **数名患者** 沟通",
                icon=":material/counter_1:",
            )
            st.info("问诊完毕后请输入 **我问完了**", icon=":material/counter_2:")
            st.info("回答患者提出的 **相关问题**", icon=":material/counter_3:")
            st.info("请认真 **填写信息** 及 **选择模式**", icon=":material/counter_4:")
            st.info(
                "作为一名 **学生**，您的过程将 **被统计**",
                icon=":material/counter_5:",
            )

        case Role.TEACHER:
            st.info(
                "作为一名 **教师**，可以进行 **模型研究**", icon=":material/counter_1:"
            )
        case Role.ADMIN:
            st.info(
                "作为一名 **管理员**，可以进行 **项目设置**",
                icon=":material/counter_1:",
            )


def show_chat(messages):
    for message in messages:
        if message["role"] == "user":
            with st.chat_message("医生"):
                st.markdown(message["content"])
        if message["role"] == "assistant":
            with st.chat_message("患者"):
                st.markdown(message["content"])


def show_patient_info(patient):
    info_df = read_patients("data/patients.json")
    info = info_df.query(
        f"server == '{patient.server}' & model == '{patient.model}' & id == '{patient.id}'"
    )["info"].tolist()[0]
    st.markdown(":book: **患者信息**")
    for key, value in info.items():
        st.markdown(f"**{key}：** {value}")


def show_result(doctor):
    with st.container(border=True):
        if doctor.role == Role.STUDENT:
            col_name, col_grade, col_major = st.columns(3)
            with col_name:
                st.markdown(f"**姓名:** {doctor.name}")
            with col_grade:
                st.markdown(f"**年级**: {doctor.grade}")
            with col_major:
                st.markdown(f"**专业**: {doctor.major}")
        col_begin, col_end, col_duration = st.columns(3)
        with col_begin:
            st.markdown(
                f":material/line_start_circle: {doctor.patients[0].begin_time.strftime("%Y-%m-%d %H:%M:%S")}"
            )
        with col_end:
            st.markdown(
                f":material/line_end_circle: {doctor.patients[-1].end_time.strftime("%Y-%m-%d %H:%M:%S")}"
            )
        with col_duration:
            st.markdown(
                f":stopwatch: {(doctor.patients[-1].end_time-doctor.patients[0].begin_time).seconds} 秒"
            )

    total_inquiry_count = 0
    total_questions_count = 0
    score = 0
    normal_inquiry_count = len(doctor.patients)

    for i, patient in enumerate(doctor.patients):
        st.divider()
        col_question_left, col_center, col_question_right = st.columns(3)
        with col_question_left:
            st.markdown(f"**:ok_woman: {i+1}/{len(doctor.patients)}**")
        with col_center:
            st.markdown(f"**{patient.begin_time.strftime("%Y-%m-%d %H:%M:%S")}**")
        with col_question_right:
            st.markdown(
                f"**:stopwatch: {(patient.end_time - patient.begin_time).seconds} 秒 🗣️ {(patient.chat_duration_time).seconds} 秒**"
            )

        with st.container(border=True):
            show_patient_info(patient)

        with st.container(border=True):
            st.markdown(":clipboard: **对话记录**")
            st.markdown(f"**:repeat: {patient.inquiry_count}**")
            total_inquiry_count += patient.inquiry_count
            show_chat(patient.messages)
        for question in patient.questions:
            total_questions_count += 1
            st.markdown(f"**Q{total_questions_count}: {question['question']}**")
            st.markdown(f"答案选项: 🔹{' 🔹'.join(question['answers'])}")
            st.markdown(f"正确答案: :white_check_mark:**{question['correct_answer']}**")
            if question["correct_answer"] == question["answer"]:
                st.markdown(f"用户回答: :white_check_mark:**{question['answer']}**")
                score += 1
            else:
                st.markdown(f"用户回答: :x:**:red[{question['answer']}]**")

    st.divider()

    question_score = round(score / total_questions_count * 100)
    inquiry_score = (total_inquiry_count - normal_inquiry_count) * 2
    st.markdown(f"**问题得分: {score} :material/pen_size_2: {
                total_questions_count} :material/close:100 :material/equal: {question_score}**")
    st.markdown(f"**复问扣分: ( {total_inquiry_count} - {
                normal_inquiry_count} ) :material/close:2 :material/equal: {inquiry_score}**")
    st.markdown(f"**最后得分: :small_orange_diamond: :red[{
                question_score - inquiry_score}] :small_orange_diamond:**")


# def show_character_info(character):
#     with st.container(border=False):
#         col_left, col_right = st.columns([1, 3])
#         with col_right:
#             with st.container(border=True):
#                 st.markdown(f"姓名: **{character['name']}**")
#                 st.markdown(f"建立: **{str(character['gmtCreate']).split(' ')[0]}**")
#                 st.markdown(f"更新: **{str(character['gmtModified']).split(' ')[0]}**")
#                 basicinfo = st.text_area(
#                     label="**基本信息**",
#                     height=500,
#                     value=character["basicInformation"],
#                 )
#         with col_left:
#             avatar_url = "http:" + character["avatar"]["fileUrl"]
#             st.image(avatar_url, caption=character["name"], use_column_width=True)

#             if st.button("**刷新**", use_container_width=True):
#                 st.rerun()
#             if st.button("**更新**", use_container_width=True):
#                 character["basicInformation"] = basicinfo
#                 xingchen = XingChen()
#                 result = xingchen.update(character)
#                 if result:
#                     st.markdown("**:green[成功...]**")
#                 else:
#                     st.markdown("**:red[失败...]**")

