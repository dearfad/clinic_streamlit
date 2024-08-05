import streamlit as st
from libs.bvcpage import set_page_header, show_result

set_page_header()

user = st.session_state.user

show_result(user)

if st.button("返回首页", use_container_width=True):
    st.switch_page("breast.py")
