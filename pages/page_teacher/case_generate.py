import streamlit as st

from pages.page_libs.prompt import page_prompt_manager
from pages.page_libs.case import page_case_manager
from libs.bvcmodels import chat
from libs.bvcdatabase import (
    create_case,
    read_caseprompt_memo,
    read_category,
    delete_case,
)

def page_case_generate():
    col_caseprompt, col_case = st.columns(2)
    with col_caseprompt:
        page_prompt_manager(table="caseprompt")
    with col_case:
        page_case_manager(page='case_generate')
        case_config = st.text_input("**病例设定**", value="乳房疾病", key='generate_case_config')
        col_case_generate, col_case_save, col_case_delete = st.columns(3)
        with col_case_generate:
            if st.button("生成病历", use_container_width=True):
                disease = case_config if case_config else "任意疾病"
                messages = [
                    {
                        "role": "system",
                        "content": st.session_state.caseprompt,
                    },
                    {
                        "role": "user",
                        "content": disease,
                    },
                ]
                with st.session_state.info_placeholder:
                    with st.spinner("思考中..."):
                        response = chat(
                            module=st.session_state.caseprompt_model_dict["module"],
                            modelname=st.session_state.caseprompt_model_dict["name"],
                            messages=messages,
                        )
                st.session_state.generated_case = response
                st.rerun()
        with col_case_save:
            if st.button("保存病历", use_container_width=True):
                create_case(
                    caseprompt=read_caseprompt_memo(st.session_state.caseprompt_memo),
                    category=read_category(book, chapter, subject),
                    creator=st.session_state.user,
                    profile=case_config,
                    content=case_content,
                )
                st.toast("Case Saved...")
        with col_case_delete:
            if st.button("删除病历", use_container_width=True):
                delete_case(id=case_dict["id"])
                st.toast("Case Deleted...")
