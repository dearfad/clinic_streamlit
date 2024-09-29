import streamlit as st

from libs.bvcclasses import Role, User
from libs.bvcdatabase import check_user_exist, user_login, get_user_role
from libs.bvcpage import set_page_header, show_role_info, set_current_user
from libs.bvcutils import  validate_register

set_page_header()

role = st.selectbox("**类别**", Role)

show_role_info(role)

match role:
    case Role.VISITOR:
        if st.button("**开始**", use_container_width=True):
            st.session_state.doctor = User()
            st.switch_page("pages/inquiry.py")

    case Role.STUDENT:
        mode = st.selectbox("**模式**", ("课堂学习", "自学测试", "出科考试"))
        name = st.text_input("**姓名**", "学生")
        grade = st.selectbox("**年级**", (range(2015, 2030, 1)))
        major = st.selectbox(
            "**专业**", ("临床医学 5+3 一体化", "临床医学 5 年制", "放射医学", "其他")
        )
        if st.button("**开始**", use_container_width=True):
            st.session_state.doctor = User(
                role=role, mode=mode, name=name, grade=grade, major=major
            )
            st.switch_page("pages/inquiry.py")

    case Role.TEACHER:
        if st.session_state.user not in ['游客','管理员']:
            role = get_user_role(st.session_state.user)
            if role == 'teacher':
                st.switch_page("pages/teacher.py")
        else:
            username = st.text_input("**用户名**")
            password = st.text_input("**密码**", type="password")        
            user_exist = check_user_exist(username)
            col_register, col_login = st.columns(2)
            with col_register:
                if st.button("**注册**", use_container_width=True, type="primary", disabled=user_exist):
                    if password and username:
                        validate_register(username, password)
                    else:
                        st.warning(":material/key: 请输入**用户名**和**密码**")
            with col_login:
                if st.button("**登录**", use_container_width=True, disabled=not user_exist):
                    if user_login(username, password):
                        with st.empty():
                            set_current_user(st.session_state.cookiecontroller, name=username)
                        st.switch_page("pages/teacher.py")
                    else:
                        st.warning(":material/key: **密码错误**")

    case Role.ADMIN:
        if st.session_state.user == '管理员':
            st.switch_page("pages/admin.py")
        else:
            password = st.text_input("**密码**", type="password")
            if st.button("**登录**", use_container_width=True):
                if password == st.secrets["admin_key"]:
                    with st.empty():
                        set_current_user(st.session_state.cookiecontroller, name="管理员")
                    st.switch_page("pages/admin.py")
                else:
                    st.warning(":material/key: **密码错误**，请咨询**管理员**相关信息")
