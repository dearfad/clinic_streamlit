import streamlit as st

from libs.bvcpage import set_page_header, set_page_footer
from pages.page_teacher.case_view import page_case_view
from pages.page_teacher.case_generate import page_case_generate
from pages.page_teacher.test_generate import page_test_generate
from pages.page_teacher.sim_patient import page_sim_patient
from pages.page_teacher.ask_answer import page_ask_answer

set_page_header(layout="wide")


with st.container(border=False):
    col_title, col_info = st.columns(2)
    with col_title:
        st.markdown("##### :material/view_headline: 模型研究 :material/view_headline:")
    with col_info:
        st.session_state.info_placeholder = st.empty()

(
    tab_case_view,
    tab_case_generate,
    tab_question_generate,
    tab_sim_patient,
    tab_ask_answer,
) = st.tabs(["病例浏览", "病例生成", "问题生成", "病例问诊", "问答分析"])

with tab_case_view:
    page_case_view()

with tab_case_generate:
    page_case_generate()

with tab_question_generate:
    page_test_generate()

with tab_sim_patient:
    page_sim_patient()

with tab_ask_answer:
    pass
    # page_ask_answer()

set_page_footer()
