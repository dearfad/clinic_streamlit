import streamlit as st

from libs.bvcdatabase import (
    create_test,
    read_case,
    read_table,
    read_testprompt_memo,
)
from libs.bvcmodels import chat
from pages.page_libs.prompt import page_prompt_manager


def page_test_generate():
    col_testprompt, col_case, col_test = st.columns(3)

    with col_testprompt:
        page_prompt_manager(table="testprompt")

    with col_case:
        if "case_content" not in st.session_state:
            st.session_state.case_content = ""

        cases = read_table("case").to_dict(orient="records")
        case_dict = st.selectbox(
            label="**选择病例**",
            options=cases,
            format_func=lambda x: x["profile"],
            key="case_dict",
        )

        tab_markdown, tab_text_area = st.tabs(["查看", "编辑"])
        with tab_markdown:
            with st.container(height=542):
                st.markdown(case_dict["content"])
        with tab_text_area:
            st.text_area(
                "**病例**",
                value=case_dict["content"],
                height=540,
                label_visibility="collapsed",
                key="text_case_content",
            )

    #### TEST CONTENT ###################################################################
    with col_test:
        test_profile = st.text_input("**问题设定**", key="test_profile")

        tab_test_content_markdown, tab_test_content = st.tabs(["查看", "编辑"])

        if "generated_test" not in st.session_state:
            st.session_state.generated_test = ""

        with tab_test_content:
            test_content = st.text_area(
                "**题目**",
                height=480,
                label_visibility="collapsed",
                value=st.session_state.generated_test,
                key="test_content",
            )

        with tab_test_content_markdown:
            with st.container(height=482):
                st.markdown(test_content)

        col_test_generate, col_test_save = st.columns(2)
        with col_test_generate:
            if st.button("生成问题", use_container_width=True):
                messages = [
                    {
                        "role": "system",
                        "content": st.session_state.testprompt,
                    },
                    {
                        "role": "user",
                        "content": case_dict["content"]
                        + f"/n **问题设定**: {test_profile}",
                    },
                ]
                with st.session_state.info_placeholder:
                    with st.spinner("思考中..."):
                        response = chat(
                            module=st.session_state.testprompt_model_dict["module"],
                            modelname=st.session_state.testprompt_model_dict["name"],
                            messages=messages,
                        )
                st.session_state.generated_test = response
                st.rerun()
        with col_test_save:
            if st.button("保存问题", use_container_width=True, key="create_test"):
                create_test(
                    testprompt=read_testprompt_memo(st.session_state.testprompt_memo),
                    case=read_case(case_dict["id"]),
                    creator=st.session_state.user,
                    profile=test_profile,
                    content=test_content,
                )
                st.toast("Case Saved...")
