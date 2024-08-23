import streamlit as st
from libs.bvcclasses import Role, Doctor
from libs.bvcpage import set_page_header
# from libs.bvcutils import reset_session_state


set_page_header()


# if "user" in st.session_state:
#     reset_session_state()
#     st.rerun()

role = st.selectbox("**类别**", Role)

match role:
    case Role.VISITOR:
        st.info(
            "请用 **正常语气** 与 **随机一名患者** 沟通", icon=":material/counter_1:"
        )

        st.info("问诊完毕后请输入 **我问完了**", icon=":material/counter_2:")

        st.info("回答患者提出的 **相关问题**", icon=":material/counter_3:")

        st.info("作为一名 **游客**，您的过程 **不被统计**", icon=":material/counter_4:")

        if st.button("**开始**", use_container_width=True):
            st.session_state.doctor = Doctor()
            st.write(st.session_state.doctor)
            # st.switch_page("pages/inquiry.py")

    case Role.STUDENT:
        name = st.text_input("**姓名**", "学生")
        grade = st.selectbox("**年级**", (range(2016, 2030, 1)))
        major = st.selectbox("**专业**", ("临床医学", "放射", "口腔", "其他"))
        mode = st.selectbox("**模式**", ("课堂学习", "自学测试", "出科考试"))

    #         match mode:
    #             case _:
    #                 st.info(
    #                     "请用 **正常语气** 与 **数名患者** 沟通",
    #                     icon=":material/counter_1:",
    #                 )

    #                 st.info("问诊完毕后请输入 **我问完了**", icon=":material/counter_2:")

    #                 st.info("回答患者提出的 **相关问题**", icon=":material/counter_3:")

    #                 st.info(
    #                     "请认真 **填写信息** 及 **选择模式**", icon=":material/counter_4:"
    #                 )

    #                 st.info(
    #                     "作为一名 **学生**，您的过程将 **被统计**",
    #                     icon=":material/counter_5:",
    #                 )

    #         if st.button("**开始**", use_container_width=True):
    #             st.session_state.user = Doctor(role, chapter, name, grade, major, mode)

    #             st.session_state.user.create_chatlog()

    #             st.switch_page("pages/inquiry.py")

    case Role.TEACHER:
        password = st.text_input("**密码**", type="password")

    #         st.info(
    #             "作为一名 **教师**，可以 **浏览分析** 数据", icon=":material/counter_1:"
    #         )

    #         if st.button("**登录**", use_container_width=True):
    #             if password == st.secrets["teacher_key"]:
    #                 st.switch_page("pages/teacher.py")
    #             else:
    #                 st.warning(":material/key: **密码错误**，请咨询**管理员**相关信息")

    case Role.ADMIN:
        password = st.text_input("**密码**", type="password")

#         st.info(
#             "作为一名 **管理员**，可以进行 **项目设置**", icon=":material/counter_1:"
#         )

#         if st.button("**登录**", use_container_width=True):
#             if password == st.secrets["admin_key"]:
#                 st.switch_page("pages/admin.py")
#             else:
#                 st.warning(":material/key: **密码错误**，请咨询**管理员**相关信息")
