import streamlit as st

from libs.bvcdatabase import read_use_model, read_prompt
from libs.bvcmodels import chat
from libs.bvcpage import show_chat
from datetime import datetime


def page_sim_patient():
    col_sim_prompt, col_ask_prompt = st.columns(2)
    models = read_use_model()
    with col_sim_prompt:
        simprompts = read_prompt(category="sim", creator=st.session_state.user)
        sim_prompt_dict = st.selectbox(
            label="**模拟提示词**",
            options=simprompts,
            format_func=lambda x: f"{x["memo"]} == {x['model']}",
        )
        sim_model_dict = st.selectbox(
            label="**模拟模型**",
            options=models,
            format_func=lambda x: x["name"],
        )
    with col_ask_prompt:
        askprompts = read_prompt(category="ask", creator=st.session_state.user)
        ask_prompt_dict = st.selectbox(
            label="**问答提示词**",
            options=askprompts,
            format_func=lambda x: f"{x["memo"]} == {x['model']}",
        )
        ask_model_dict = st.selectbox(
            label="**问答模型**",
            options=models,
            format_func=lambda x: x["name"],
        )

    if "sim_messages" not in st.session_state:
        st.session_state.sim_messages = [
            {
                "role": "system",
                "content": sim_prompt_dict['prompt'] + st.session_state.case_content + st.session_state.story_content,
            },
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "大夫，你好"},
        ]

    tab_sim, tab_temp = st.tabs(["模拟对话", "患者对话"])
    with tab_sim:
        chat_placeholder = st.container(border=True, height=386)
        with chat_placeholder:
            show_chat(st.session_state.sim_messages)
    with tab_temp:
        pass

    if user_prompt := st.chat_input(""):
            with chat_placeholder:
                with st.chat_message("医生"):
                    st.markdown(user_prompt)
            st.session_state.sim_messages.append({"role": "user", "content": user_prompt})
            start_time = datetime.now()
            with st.session_state.info_placeholder:
                with st.spinner("思考中..."):
                    response = chat(
                        module=sim_model_dict["module"],
                        modelname=sim_model_dict["name"],
                        messages=st.session_state.sim_messages,
                    )
            chat_placeholder.markdown(
                f":stopwatch: {round((datetime.now()-start_time).total_seconds(),2)} 秒"
            )
            with chat_placeholder:
                with st.chat_message("患者"):
                    st.markdown(response)
            st.session_state.sim_messages.append(
                {"role": "assistant", "content": response}
            )

    if st.button("清除对话", key="clear_sim_chat", use_container_width=True):
        del st.session_state.sim_messages
        st.rerun()
