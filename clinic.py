import streamlit as st

from libs.bvcclasses import Role
from libs.bvcdatabase import read_user_role, read_user_exist, create_user, read_user_login
from libs.bvcpage import set_page_header

set_page_header()

role = st.selectbox("**类别**", Role)

match role:
    case Role.VISITOR:
        pass
        # if st.button("**开始**", use_container_width=True):
        #     st.session_state.doctor = User()
        #     st.switch_page("pages/inquiry.py")

    case Role.STUDENT:
        pass
        # mode = st.selectbox("**模式**", ("课堂学习", "自学测试", "出科考试"))
        # name = st.text_input("**姓名**", "学生")
        # grade = st.selectbox("**年级**", (range(2015, 2030, 1)))
        # major = st.selectbox(
        #     "**专业**", ("临床医学 5+3 一体化", "临床医学 5 年制", "放射医学", "其他")
        # )
        # if st.button("**开始**", use_container_width=True):
        #     st.session_state.doctor = User(
        #         role=role, mode=mode, name=name, grade=grade, major=major
        #     )
        #     st.switch_page("pages/inquiry.py")

    case Role.TEACHER:
        if st.session_state.user not in ['访客','管理员']:
            role = read_user_role(st.session_state.user)
            if role == 'teacher':
                st.switch_page("pages/teacher.py")
            else:
                st.warning(":material/key: **请咨询管理员提升权限**")
                if st.button("**退出登录**", use_container_width=True):
                    del st.session_state.user
                    st.rerun()
        else:
            username = st.text_input("**用户名**")
            password = st.text_input("**密码**", type="password")        
            user_exist = read_user_exist(username)
            col_register, col_login = st.columns(2)
            with col_register:
                if st.button("**注册**", use_container_width=True, type="primary", disabled=user_exist):
                    if password and username:
                        create_user(username, password)
                        st.rerun()
                    else:
                        st.warning(":material/key: 请输入**用户名**和**密码**")
            with col_login:
                if st.button("**登录**", use_container_width=True, disabled=not user_exist):
                    if read_user_login(username, password):
                        st.session_state.user = username
                        role = read_user_role(st.session_state.user)
                        if role == 'teacher':
                            st.switch_page("pages/teacher.py")
                        else:
                            st.rerun()
                    else:
                        st.warning(":material/key: **密码错误**")

    case Role.ADMIN:
        if st.session_state.user == '管理员':
            st.switch_page("pages/admin.py")
        else:
            password = st.text_input("**密码**", type="password")
            if st.button("**登录**", use_container_width=True):
                if password == st.secrets["admin_key"]:
                    st.session_state.user = '管理员'
                    st.switch_page("pages/admin.py")
                else:
                    st.warning(":material/key: **密码错误**，请咨询**管理员**相关信息")
