import streamlit as st

from libs.bvcpage import set_page_footer, set_page_header

set_page_header()

with st.sidebar:
    st.markdown('##### 教师主页')
    st.markdown('##### 教师主页')
st.markdown('##### 教学研究')
st.page_link('pages/models.py', label='模型研究', icon="🌎")

set_page_footer()