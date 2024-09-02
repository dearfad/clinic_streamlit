import streamlit as st
from libs.bvcpage import set_page_header
# from libs.bvcutils import user_info_formatter, load_data

set_page_header()

st.markdown('##### 教学研究')
st.page_link('pages/models.py', label='模型研究', icon="🌎")

if st.button("返回首页", use_container_width=True):
    st.switch_page("bvc.py")