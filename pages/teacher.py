import streamlit as st
from libs.bvcpage import set_page_header, show_result
from libs.bvcutils import user_info_formatter, load_data


set_page_header()

mode = st.selectbox("**模式**", ("记录浏览", "理论授课", "教学研究"))

users = load_data()

match mode:
    case '记录浏览':
        user = st.selectbox(
                "**用户**",
                users,
                format_func=lambda x: user_info_formatter(x),
            )

        show_result(user)
    case _:
        pass

if st.button("返回首页", use_container_width=True):
    st.switch_page("breast.py")