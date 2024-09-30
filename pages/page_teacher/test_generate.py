import streamlit as st
from libs.bvcdatabase import (
    read_table,
    create_prompt,
    delete_prompt,
    read_category,
    read_caseprompt_memo,
    read_prompt,
    read_use_model,
    create_case,
    read_category_field,
    update_prompt,
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

        cases = read_table('case').to_dict(orient="records")
        case_dict = st.selectbox(
            label="选择案例",
            options=cases,
            format_func=lambda x: x['profile'],
            key="case_dict",
        )

        tab_markdown, tab_text_area = st.tabs(["编辑", "查看"])
        with tab_markdown:
            with st.container(height=402):
                st.markdown(case_dict['content'])
        with tab_text_area:
            st.text_area(
            "**病例**",
            value=case_dict['content'],
            height=400,
            label_visibility="collapsed",
            key="text_case_content",
        )
        

    #### TEST CONTENT ###################################################################
    with col_test:
        test_selection = st.selectbox("**选择问题**", options=[1,2,3])
        tab_test_content, tab_test_content_markdown = st.tabs(["编辑", "查看"])

        if "generated_test" not in st.session_state:
            st.session_state.generated_test = ""
        

        with tab_test_content:
            test_content = st.text_area(
                "**题目**",
                height=400,
                label_visibility="collapsed",
                value=st.session_state.generated_test,
                key="test_content",
            )
        with tab_test_content_markdown:
            with st.container(height=402):
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
                        "content": case_dict['content'],
                    },
                ]
                with st.spinner("思考中..."):
                    response = chat(
                        module=st.session_state.testprompt_model_dict["module"],
                        modelname=st.session_state.testprompt_model_dict["name"],
                        messages=messages,
                    )
                st.session_state.generated_test = response
                st.rerun()
        with col_test_save:
            pass
            # if st.button("保存病历", use_container_width=True):
            #     create_case(
            #         teacher=read_caseprompt_memo(caseprompt_memo),
            #         category=read_category(book, chapter, subject),
            #         creator=st.session_state.user,
            #         profile=test_config,
            #         content=test_content,
            #     )
            #     st.toast("Case Saved...")
