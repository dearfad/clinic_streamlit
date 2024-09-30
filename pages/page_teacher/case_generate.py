import streamlit as st

from libs.bvcdatabase import (
    read_category,
    read_caseprompt_memo,
    create_case,
    read_category_field,
)
from libs.bvcmodels import chat
from pages.page_libs.prompt import page_prompt_manager


def page_case_generate():
    col_caseprompt, col_case = st.columns(2)

    #### CASE PROMPT ###################################################################
    with col_caseprompt:
        page_prompt_manager(table="caseprompt")

    #### CASE CONTENT ###################################################################
    with col_case:
        case_config = st.text_input("**病例设定**", value="乳房疾病")
        tab_case_content, tab_case_content_markdown = st.tabs(["编辑", "查看"])

        if "generated_case" not in st.session_state:
            st.session_state.generated_case = ""
        

        with tab_case_content:
            case_content = st.text_area(
                "**病例**",
                height=400,
                label_visibility="collapsed",
                value=st.session_state.generated_case,
                key="case_content",
            )
        with tab_case_content_markdown:
            with st.container(height=402):
                st.markdown(case_content)

        cols = st.columns(3)
        with cols[0]:
            book = st.selectbox("**教科书**", read_category_field("book"))
        with cols[1]:
            chapter = st.selectbox("**章节**", read_category_field("chapter"))
        with cols[2]:
            subject = st.selectbox("**主题**", read_category_field("subject"))

        col_case_generate, col_case_save = st.columns(2)
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
