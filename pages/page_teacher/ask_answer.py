import streamlit as st

from pages.page_libs.prompt import page_prompt_manager
from libs.bvcdatabase import read_table, read_case_test
from libs.bvcpage import show_chat
from datetime import datetime
from libs.bvcmodels import chat

def page_ask_answer():
    col_askprompt, col_case, col_ask_answer = st.columns(3)

    #### CASE PROMPT ###################################################################
    with col_askprompt:
        page_prompt_manager(table="askprompt")

    with col_case:
        if "case_content" not in st.session_state:
            st.session_state.case_content = ""

        cases = read_table("case").to_dict(orient="records")
        test_case_dict = st.selectbox(
            label="**选择病例**",
            options=cases,
            format_func=lambda x: x["profile"],
            key="test_case_dict",
        )

        tab_markdown, tab_text_area, tab_tests = st.tabs(["查看", "编辑","问题"])
        with tab_markdown:
            with st.container(height=542):
                st.markdown(test_case_dict["content"])
        with tab_text_area:
            st.text_area(
                "**病例**",
                value=test_case_dict["content"],
                height=540,
                label_visibility="collapsed",
                key="ask_text_case_content",
            )
        with tab_tests:
            with st.container(height=542):
                case_test= read_case_test(test_case_dict['id'])
                if case_test:
                    st.markdown(case_test[0].content)
    
    with col_ask_answer:
        if "ask_messages" not in st.session_state:
            st.session_state.ask_messages = [
                {
                    "role": "system",
                    "content": st.session_state.askprompt + "\n" + case_test[0].content,
                },
                # {
                #     "role": "user",
                #     "content": "请开始问答吧",
                # },
            ]

        ask_placeholder = st.container(border=True, height=576)
        with ask_placeholder:
            show_chat(st.session_state.ask_messages)
        # if st.button('开始问答', use_container_width=True):
        #     with st.session_state.info_placeholder:
        #             with st.spinner("思考中..."):
        #                 response = chat(
        #                     module=st.session_state.askprompt_model_dict["module"],
        #                     modelname=st.session_state.askprompt_model_dict["name"],
        #                     messages=st.session_state.ask_messages,
        #                 )
        #     st.session_state.ask_messages.append(
        #             {"role": "assistant", "content": response}
        #         )
        if prompt := st.chat_input("", key='ask_chat_input'):
                with ask_placeholder:
                    with st.chat_message("医生"):
                        st.markdown(prompt)
                st.session_state.ask_messages.append({"role": "user", "content": prompt})
                start_time = datetime.now()
                with st.session_state.info_placeholder:
                    with st.spinner("思考中..."):
                        response = chat(
                            module=st.session_state.askprompt_model_dict["module"],
                            modelname=st.session_state.askprompt_model_dict["name"],
                            messages=st.session_state.ask_messages,
                        )
                ask_placeholder.markdown(
                    f":stopwatch: {round((datetime.now()-start_time).total_seconds(),2)} 秒"
                )
                with ask_placeholder:
                    with st.chat_message("患者"):
                        st.markdown(response)
                st.session_state.ask_messages.append(
                    {"role": "assistant", "content": response}
                )

        if st.button("清除对话", key="clear_ask_chat", use_container_width=True):
            del st.session_state.ask_messages
            st.rerun()
