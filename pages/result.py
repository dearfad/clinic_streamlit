import streamlit as st
from libs.bvcpage import set_page_header, show_result

set_page_header()

doctor = st.session_state.doctor

show_result(doctor)

if st.button("返回首页", use_container_width=True):
    st.switch_page("bvc.py")
