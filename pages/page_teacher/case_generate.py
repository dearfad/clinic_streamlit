import streamlit as st

from libs.bvcdatabase import (
    create_case,
    read_caseprompt_memo,
    read_category,
    read_category_field,
)
from libs.bvcmodels import chat
from pages.page_libs.prompt import page_prompt_manager
from pages.page_libs.case import page_case_manager


def page_case_generate():
    col_caseprompt, col_case = st.columns(2)

    #### CASE PROMPT ###################################################################
    with col_caseprompt:
        page_prompt_manager(table="caseprompt")

    #### CASE CONTENT ###################################################################
    with col_case:
        page_case_manager()