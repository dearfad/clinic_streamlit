import streamlit as st

from libs.bvcmodels import chat
from libs.bvcdatabase import (
    read_prompt,
    create_case,
    read_use_model,
)


def page_case_generate():
    col_caseprompt, col_testprompt, col_storyprompt = st.columns(3)
    models = read_use_model()
    with col_caseprompt:
        caseprompts = read_prompt("caseprompt", st.session_state.user)

        caseprompt_dict = st.selectbox(
            label="**病历提示词**",
            options=caseprompts,
            format_func=lambda x: f"{x["memo"]} == {x['model']} == {x['creator']}",
        )
        case_profile = st.text_input("**病例设定**", value="乳房疾病")

        case_model_dict = st.selectbox(
            label="**病历模型**",
            options=models,
            format_func=lambda x: x["name"],
        )

    with col_testprompt:
        testprompts = read_prompt("testprompt", st.session_state.user)

        testprompt_dict = st.selectbox(
            label="**问题提示词**",
            options=testprompts,
            format_func=lambda x: f"{x["memo"]} == {x['model']} == {x['creator']}",
        )
        test_profile = st.text_input("**问题设定**", value="乳腺癌")
        test_model_dict = st.selectbox(
            label="**问题模型**",
            options=models,
            format_func=lambda x: x["name"],
        )

    with col_storyprompt:
        storyprompts = read_prompt("storyprompt", st.session_state.user)

        storyprompt_dict = st.selectbox(
            label="**故事提示词**",
            options=storyprompts,
            format_func=lambda x: f"{x["memo"]} == {x['model']} == {x['creator']}",
        )
        story_profile = st.text_input("**故事设定**", value="悲惨")
        story_model_dict = st.selectbox(
            label="**故事模型**",
            options=models,
            format_func=lambda x: x["name"],
        )

    if "generated_case" not in st.session_state:
        st.session_state.generated_case = ""
    if "generated_test" not in st.session_state:
        st.session_state.generated_test = ""
    if "generated_story" not in st.session_state:
        st.session_state.generated_story = ""

    with st.container(height=366):
            st.markdown('**预览病历**')
            st.markdown(st.session_state.generated_case)
            st.markdown('**预览问题**')
            st.markdown(st.session_state.generated_test)
            st.markdown('**预览故事**')
            st.markdown(st.session_state.generated_story)

    col_case_generate, col_case_save = st.columns(2)
    with col_case_generate:
        if st.button("生成病历", use_container_width=True):
            disease = case_profile if case_profile else "任意疾病"
            messages = [
                {
                    "role": "system",
                    "content": caseprompt_dict["prompt"],
                },
                {
                    "role": "user",
                    "content": disease,
                },
            ]
            with st.session_state.info_placeholder:
                with st.spinner("病历生成中..."):
                    response = chat(
                        module=case_model_dict["module"],
                        modelname=case_model_dict["name"],
                        messages=messages,
                    )
            st.session_state.generated_case = response

            messages = [
                {
                    "role": "system",
                    "content": testprompt_dict["prompt"],
                },
                {
                    "role": "user",
                    "content": st.session_state.generated_case
                    + f"/n **问题设定**: {test_profile}",
                },
            ]

            with st.session_state.info_placeholder:
                with st.spinner("问题生成中..."):
                    response = chat(
                        module=test_model_dict["module"],
                        modelname=test_model_dict["name"],
                        messages=messages,
                    )
            st.session_state.generated_test = response

            messages = [
                {
                    "role": "system",
                    "content": storyprompt_dict["prompt"],
                },
                {
                    "role": "user",
                    "content": st.session_state.generated_case
                    + f"/n **故事设定**: {story_profile}",
                },
            ]

            with st.session_state.info_placeholder:
                with st.spinner("故事生成中..."):
                    response = chat(
                        module=story_model_dict["module"],
                        modelname=story_model_dict["name"],
                        messages=messages,
                    )
            st.session_state.generated_story = response
            st.rerun()
    with col_case_save:
        if st.button("保存病历", use_container_width=True):
            create_case(
                creator=st.session_state.user,
                profile=case_profile,
                content=st.session_state.generated_case,
                test=st.session_state.generated_test,
                story=st.session_state.generated_story,
                book="待定",
                chapter="待定",
                subject="待定",
            )
            st.toast("Case Saved...")
