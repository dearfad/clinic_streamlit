import streamlit as st

from libs.bvcpage import set_page_header, set_page_footer
from pages.page_teacher.case_manager import page_case_manager
from pages.page_teacher.case_generate import page_case_generate
from pages.page_teacher.prompt_manager import page_prompt_manager
from pages.page_teacher.sim_patient import page_sim_patient

set_page_header(layout="wide")


with st.container(border=False):
    col_title, col_info = st.columns(2)
    with col_title:
        st.markdown("##### :material/view_headline: 模型研究 :material/view_headline:")
    with col_info:
        st.session_state.info_placeholder = st.empty()

col_case, col_sim, col_generate, col_prompt = st.columns(4)

with col_case:
    page_case_manager()

with col_sim:
    page_sim_patient()

with col_generate:
    page_case_generate()

with col_prompt:
    page_prompt_manager()


set_page_footer()
