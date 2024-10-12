import streamlit as st

from pages.page_libs.prompt import page_prompt_manager
from pages.page_libs.case import page_case_manager


def page_case_generate():
    col_caseprompt, col_case = st.columns(2)
    with col_caseprompt:
        page_prompt_manager(table="caseprompt")
    with col_case:
        page_case_manager()