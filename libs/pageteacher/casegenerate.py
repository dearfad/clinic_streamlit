import streamlit as st
from libs.bvcdatabase import (
    delete_prompt,
    create_prompt,
    read_use_model,
    read_prompt,
    update_prompt,
    create_case,
    read_caseprompt_memo,
    read_category,
    get_user,
    read_category_field_distinct,
)
from libs.bvcmodels import chat

def page_case_generate():
    st.title("病例生成")
    col_teacher_prompt, col_case_content = st.columns(2)
    ##########################################
    with col_teacher_prompt:
        teacher_prompt_dict = st.selectbox(
            "**教师提示词**",
            read_prompt(st.session_state.user),
            format_func=lambda x: f"{x["memo"]} == {x['model']} == {x['creator']}",
        )

        tab_text_area, tab_markdown = st.tabs(["编辑", "查看"])
        with tab_text_area:
            teacher_prompt = st.text_area(
                "**提示词**",
                value=teacher_prompt_dict["prompt"],
                height=450,
                label_visibility="collapsed",
            )
        with tab_markdown:
            with st.container(height=452):
                st.markdown(teacher_prompt)

        col_teacher_memo, col_teacher_public, col_teacher_model, col_teacher_creator = st.columns(4)
        with col_teacher_memo:
            teacher_prompt_memo = st.text_input(
                "**备注**", value=teacher_prompt_dict["memo"]
            )
        with col_teacher_public:
            teacher_public = st.selectbox(
                "**公开**",
                [False, True],
                index=teacher_prompt_dict["public"],
                format_func=lambda x: "是" if x else "否",
            )
        with col_teacher_model:
            models = read_use_model()
            try:
                names = [model["name"] for model in models]
                index = names.index(teacher_prompt_dict["model"])
            except ValueError:
                st.toast("模型不在使用，请更新！")
                index = 0
            model_dict = st.selectbox(
                "**模型**", models, index=index, format_func=lambda x: x["name"]
            )
        with col_teacher_creator:
            teacher_prompt_creator = st.text_input(
                "**作者**", value=teacher_prompt_dict["creator"], disabled=True
            )
        col_teacher_insert, col_teacher_update, col_teacher_delete = st.columns(3)
        with col_teacher_insert:
            if st.button(
                ":material/add: 添加",
                key="insert_teacher_prompt",
                use_container_width=True,
            ):
                if st.session_state.user != "游客":
                    create_prompt(
                        prompt=teacher_prompt,
                        memo=teacher_prompt_memo,
                        model=model_dict["name"],
                        creator=st.session_state.user,
                        public=teacher_public,
                    )
                    st.rerun()
                else:
                    st.toast("游客无法进行此项操作，请登录！")
        with col_teacher_update:
            if st.button(
                ":material/update: 更新",
                key="update_teacher_prompt",
                use_container_width=True,
            ):
                if st.session_state.user != "游客":
                    if st.session_state.user == teacher_prompt_creator:
                        update_prompt(
                            id=teacher_prompt_dict["id"],
                            prompt=teacher_prompt,
                            memo=teacher_prompt_memo,
                            model=model_dict["name"],
                            creator=st.session_state.user,
                            public=teacher_public,
                        )
                        st.rerun()
                    else:
                        st.toast("无权限更新提示词")
                else:
                    st.toast("游客无法进行此项操作，请登录！")
        with col_teacher_delete:
            if st.button(
                ":material/delete: 删除",
                key="delete_teacher_prompt",
                type="primary",
                use_container_width=True,
            ):
                if st.session_state.user != "游客":
                    if st.session_state.user == teacher_prompt_creator:
                        delete_prompt(id=teacher_prompt_dict["id"])
                        st.rerun()
                    else:
                        st.toast("无权限删除提示词")
                else:
                    st.toast("游客无法进行此项操作，请登录！")
    

        ########################################################################################
    with col_case_content:
        if "user_prompt" not in st.session_state:
            st.session_state.user_prompt = "乳房疾病"
        user_prompt = st.text_input("**病例设定**", value=st.session_state.user_prompt)
        if "patient_info" not in st.session_state:
            st.session_state.patient_info = ""

        tab_patient_info, tab_patient_info_markdown = st.tabs(["编辑", "查看"])
        with tab_patient_info:
            patient_info = st.text_area(
                "**病历**",
                value=st.session_state.patient_info,
                height=450,
                label_visibility="collapsed",
            )
        with tab_patient_info_markdown:
            with st.container(height=452):
                st.markdown(patient_info)


        cols = st.columns(3)
        with cols[0]:
            book = st.selectbox("**教科书**", read_category_field_distinct("book"))
        with cols[1]:
            chapter = st.selectbox("**章节**", read_category_field_distinct("chapter"))
        with cols[2]:
            subject = st.selectbox("**主题**", read_category_field_distinct("subject"))
        
        col_case_generate, col_case_save = st.columns(2)
        with col_case_generate:
            if st.button("生成病历", use_container_width=True):
                if not st.session_state.user_prompt:
                    st.session_state.user_prompt = "任意疾病"
                messages = [
                    {
                        "role": "system",
                        "content": teacher_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ]
                with st.spinner("思考中..."):
                    response = chat(
                        module=model_dict["module"],
                        modelname=model_dict["name"],
                        messages=messages,
                    )
                st.session_state.patient_info = response
                st.rerun()        
        with col_case_save:
            if st.button("保存病历", use_container_width=True):
                create_case(
                    teacher=read_caseprompt_memo(teacher_prompt_memo),
                    chapter=read_category(book, chapter, subject),
                    user=get_user(st.session_state.user),
                    profile=user_prompt,
                    content=patient_info,
                )
                st.toast("Case Saved...")