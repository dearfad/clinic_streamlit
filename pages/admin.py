import streamlit as st
from utils import set_page_header

set_page_header()

st.markdown(":material/admin_panel_settings: **管理员**")

if st.button("返回首页", use_container_width=True):
    st.switch_page("breast.py")
