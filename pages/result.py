import streamlit as st
from libs.bvcpage import set_page_header, show_setting_page, show_result

set_page_header()
show_setting_page()

doctor = st.session_state.doctor

show_result(doctor)

if st.button("返回首页", use_container_width=True):
    st.switch_page("clinic.py")
