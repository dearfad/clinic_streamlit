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
                "content": sim_prompt_dict["prompt"]
                + st.session_state.case_content
                + st.session_state.story_content
            },
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "大夫，你好"},
        ]
    if "ask_messages" not in st.session_state:
        st.session_state.ask_messages = [
            {
                "role": "system",
                "content": ask_prompt_dict["prompt"],
            },
            {"role": "user", "content": "下面是提供的选择题：\n" + st.session_state.test_content},
            # {"role": "assistant", "content": "请准备"},
        ]

    tab_sim, tab_ask = st.tabs(["模拟问诊", "模拟问答"])
    with tab_sim:
        sim_placeholder = st.container(border=True, height=386)
        with sim_placeholder:
            show_chat(st.session_state.sim_messages)
        if sim_prompt := st.chat_input("", key="sim_input"):
            with sim_placeholder:
                with st.chat_message("医生"):
                    st.markdown(sim_prompt)

            st.session_state.sim_messages.append({"role": "user", "content": sim_prompt})
            with st.session_state.info_placeholder:
                with st.spinner("思考中..."):
                    response = chat(
                        module=sim_model_dict["module"],
                        modelname=sim_model_dict["name"],
                        messages=st.session_state.sim_messages,
                    )
            with sim_placeholder:
                with st.chat_message("患者"):
                    st.markdown(response)
            st.session_state.sim_messages.append({"role": "assistant", "content": response})

    with tab_ask:
        ask_placeholder = st.container(border=True, height=386)
        with ask_placeholder:
            show_chat(st.session_state.ask_messages, loc=2)
        if ask_prompt := st.chat_input("", key="ask_input"):
            with ask_placeholder:
                with st.chat_message("医生"):
                    st.markdown(ask_prompt)
            with st.session_state.info_placeholder:
                with st.spinner("思考中..."):
                    response = chat(
                        module=ask_model_dict["module"],
                        modelname=ask_model_dict["name"],
                        messages=st.session_state.ask_messages,
                    )
            with ask_placeholder:
                with st.chat_message("患者"):
                    st.markdown(response)
            st.session_state.ask_messages.append(
                {"role": "assistant", "content": response}
            )

    if st.button("清除对话", key="clear_sim_chat", use_container_width=True):
        del st.session_state.sim_messages
        del st.session_state.ask_messages
        st.rerun()
