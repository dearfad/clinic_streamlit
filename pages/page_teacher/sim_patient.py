import streamlit as st

from pages.page_libs.prompt import page_prompt_manager
from libs.bvcdatabase import read_table
from libs.bvcmodels import chat
from libs.bvcpage import show_chat
from datetime import datetime


def page_sim_patient():
    col_simprompt, col_case, col_sim = st.columns(3)

    #### CASE PROMPT ###################################################################
    with col_simprompt:
        page_prompt_manager(table="simprompt")

    with col_case:
        if "case_content" not in st.session_state:
            st.session_state.case_content = ""

        cases = read_table("case").to_dict(orient="records")
        case_dict = st.selectbox(
            label="**选择病例**",
            options=cases,
            format_func=lambda x: x["profile"],
            key="sim_case_dict",
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
                key="text_sim_case_content",
            )

    with col_sim:
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "system",
                    "content": st.session_state.simprompt + case_dict["content"],
                },
                {"role": "user", "content": "你好"},
                {"role": "assistant", "content": "大夫，你好"},
            ]

        chat_placeholder = st.container(border=True, height=576)
        with chat_placeholder:
            show_chat(st.session_state.messages)

        if prompt := st.chat_input(""):
                with chat_placeholder:
                    with st.chat_message("医生"):
                        st.markdown(prompt)
                st.session_state.messages.append({"role": "user", "content": prompt})
                start_time = datetime.now()
                with st.session_state.info_placeholder:
                    with st.spinner("思考中..."):
                        response = chat(
                            module=st.session_state.simprompt_model_dict["module"],
                            modelname=st.session_state.simprompt_model_dict["name"],
                            messages=st.session_state.messages,
                        )
                chat_placeholder.markdown(
                    f":stopwatch: {round((datetime.now()-start_time).total_seconds(),2)} 秒"
                )
                with chat_placeholder:
                    with st.chat_message("患者"):
                        st.markdown(response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )

        if st.button("清除对话", key="clear_sim_chat", use_container_width=True):
            del st.session_state.messages
            st.rerun()
