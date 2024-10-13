import streamlit as st

from libs.bvcpage import set_page_header, set_page_footer
from pages.page_teacher.case_manager import page_case_manager
from pages.page_teacher.case_generate import page_case_generate
from pages.page_teacher.prompt_manager import page_prompt_manager
# from pages.page_teacher.sim_patient import page_sim_patient
# from pages.page_teacher.ask_answer import page_ask_answer

set_page_header(layout="wide")


with st.container(border=False):
    col_title, col_info = st.columns(2)
    with col_title:
        st.markdown("##### :material/view_headline: 模型研究 :material/view_headline:")
    with col_info:
        st.session_state.info_placeholder = st.empty()

col_case, col_prompt = st.columns(2)

with col_case:
    page_case_manager()

with col_prompt:
    tab_case_generate, tab_prompt_manager, tab_sim_patient, tab_ask_answer = st.tabs(
        ["病例生成", "提示词管理", "病例问诊", "问答分析"]
    )

    with tab_case_generate:
        page_case_generate()

    with tab_prompt_manager:
        page_prompt_manager()

    with tab_sim_patient:
        pass
        # page_sim_patient()

    with tab_ask_answer:
        pass
        # page_ask_answer()

set_page_footer()
