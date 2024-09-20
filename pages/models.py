from datetime import datetime

import streamlit as st

from libs.bvcclasses import Role, User
from libs.bvcdatabase import (
    delete_prompt,
    insert_prompt,
    # read_prompt,
    select_model,
    select_prompt,
    update_prompt,
)
from libs.bvcmodels import chat, chat_patient
from libs.bvcpage import set_page_header, show_chat

# ========== 设定 ==========
set_page_header(layout="wide")

# ========== 项目 ==========
col_research, col_user = st.columns(2)
with col_research:
    st.markdown("##### :material/view_headline: 模型研究 :material/view_headline:")
with col_user:
    if "user" not in st.session_state:
        st.session_state.user = User(role=Role.VISITOR, name="游客")
    st.markdown(f"用户名：**{st.session_state.user.name}**")

# ========== 病例设计 ==========
with st.expander(":material/cases: **病例设计**", expanded=True):
    col_teacher_prompt, col_patient_info, col_question_prompt, col_questions = (
        st.columns(4)
    )
    with col_teacher_prompt:
        teacher_prompt_dict = st.selectbox(
            "**教师提示词**",
            select_prompt("teacher", st.session_state.user.name),
            format_func=lambda x: x["memo"],
        )

        tab_text_area, tab_markdown = st.tabs(['编辑', '查看'])
        with tab_text_area:
            teacher_prompt = st.text_area(
                "**提示词**",
                value=teacher_prompt_dict["prompt"],
                height=300,
                label_visibility="collapsed",          
            )
        with tab_markdown:
            with st.container(height=302):
                st.markdown(teacher_prompt)

        col_teacher_memo, col_teacher_public = st.columns(2)
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

        col_teacher_model, col_teacher_creator = st.columns(2)
        with col_teacher_model:
            models = select_model()            
            try:
                names = [model['name'] for model in models]
                index = names.index(teacher_prompt_dict['model'])
            except ValueError:
                st.toast("模型不在使用，请更新！")
                index=0
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
                if st.session_state.user.name != "游客":
                    insert_prompt(
                        "teacher",
                        prompt=teacher_prompt,
                        memo=teacher_prompt_memo,
                        model=model_dict['name'],
                        creator=st.session_state.user.name,
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
                if st.session_state.user.name != "游客":
                    if st.session_state.user.name == teacher_prompt_creator:
                        update_prompt(
                            "teacher",
                            id=teacher_prompt_dict["id"],
                            prompt=teacher_prompt,
                            memo=teacher_prompt_memo,
                            model=model_dict['name'],
                            creator=st.session_state.user.name,
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
                if st.session_state.user.name != "游客":
                    if st.session_state.user.name == teacher_prompt_creator:
                        delete_prompt("teacher", id=teacher_prompt_dict["id"])
                        st.rerun()
                    else:
                        st.toast("无权限删除提示词")
                else:
                    st.toast("游客无法进行此项操作，请登录！")

    with col_patient_info:
        if "user_prompt" not in st.session_state:
            st.session_state.user_prompt = "乳房疾病"
        st.text_input("**病例设定**", value=st.session_state.user_prompt)
        if "patient_info" not in st.session_state:
            st.session_state.patient_info = ""
        
        tab_patient_info, tab_patient_info_markdown = st.tabs(['编辑', '查看'])
        with tab_patient_info:
            patient_info = st.text_area(
                "**病历**",
                value=st.session_state.patient_info,
                height=300,
                label_visibility="collapsed",
            )
        with tab_patient_info_markdown:
            with st.container(height=302):
                st.markdown(patient_info)

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
                    "content": st.session_state.user_prompt,
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

    with col_question_prompt:
        question_prompt_dict = st.selectbox(
            "**问题提示词**",
            select_prompt("teacher", st.session_state.user.name),
            format_func=lambda x: x["memo"],
        )
        question_prompt_memo = st.text_input(
            "**备注**", value=question_prompt_dict["memo"], key="question_prompt_memo"
        )
        # if "question_prompt" not in st.session_state:
        #     st.session_state.question_prompt = read_prompt()["question_prompt"]
        st.text_area(
            "**问题提示词**",
            key="question_prompt",
            height=400,
        )

    with col_questions:
        # if "questions" not in st.session_state:
        #     st.session_state.questions = read_prompt()["questions"]
        st.text_area(
            "**questions**",
            key="questions",
            height=260,
        )
        if st.button("出题", use_container_width=True):
            messages = [
                {
                    "role": "system",
                    "content": st.session_state.question_prompt,
                },
                {"role": "user", "content": st.session_state.patient_info},
            ]
            with st.spinner("思考中..."):
                response = chat(
                    module="zhipu", modelname="glm-4-flash", messages=messages
                )
            st.session_state.questions = response
            st.rerun()

# if "doctor" not in st.session_state:
#     st.session_state.doctor = Doctor(role=Role.TEACHER, mode="模型研究")
#     st.session_state.doctor.assign_patients()
# else:
#     st.session_state.doctor.mode = "模型研究"
#     if not st.session_state.doctor.patients:
#         st.session_state.doctor.assign_patients()
# if "chat_container" not in st.session_state:
#     st.session_state.chat_container = {}

# col_system, col_ask, col_model = st.columns(3)
# with col_system:
#     if "system_prompt" not in st.session_state:
#         st.session_state.system_prompt = read_prompt()["system_prompt"]
#     st.text_area(
#         "**system_prompt**",
#         key="system_prompt",
#         height=200,
#     )
# with col_ask:
#     if "ask_prompt" not in st.session_state:
#         st.session_state.ask_prompt = read_prompt()["ask_prompt"]
#     st.text_area(
#         "**ask_prompt**",
#         key="ask_prompt",
#         height=200,
#     )
# with col_model:
#     st.markdown("**MODELS**")
#     models = st.data_editor(
#         models_df,
#         height=280,
#         hide_index=True,
#         column_order=("use", "name"),
#         use_container_width=True,
#     )


# selected_models = models[models["use"]]["name"].to_list()
# if len(selected_models) == 0:
#     st.warning("请至少选择一个模型...")
#     st.stop()

# chat_cols = st.columns(len(selected_models))
# for i, col in enumerate(chat_cols):
#     with col:
#         st.session_state.chat_container[selected_models[i]] = st.container(
#             height=210, border=True
#         )
#         st.markdown(f"**{selected_models[i]}**")

# for patient in st.session_state.doctor.patients:
#     if not patient.messages:
#         patient.messages = [
#             {
#                 "role": "system",
#                 "content": st.session_state.system_prompt
#                 + st.session_state.patient_info,
#             },
#             {"role": "user", "content": "你好"},
#             {"role": "assistant", "content": "大夫，你好"},
#         ]
#     if patient.model.name in selected_models:
#         patient.model.use = True
#     else:
#         patient.model.use = False

#     if patient.model.use:
#         with st.session_state.chat_container[patient.model.name]:
#             show_chat(patient.messages)

# cols = st.columns(2)
# with cols[0]:
#     chat_input_placeholder = st.container()
#     if prompt := chat_input_placeholder.chat_input(""):
#         for patient in st.session_state.doctor.patients:
#             if patient.model.use:
#                 with st.session_state.chat_container[patient.model.name]:
#                     with st.chat_message("医生"):
#                         st.markdown(prompt)
#                     patient.messages.append({"role": "user", "content": prompt})
#                     start_time = datetime.now()
#                     with st.spinner("思考中..."):
#                         response = chat_patient(patient)
#                     st.markdown(
#                         f":stopwatch: {round((datetime.now()-start_time).total_seconds(),2)} 秒"
#                     )
#                     with st.chat_message("患者"):
#                         st.markdown(response)
#                     patient.messages.append({"role": "assistant", "content": response})

# with st.container(border=True):
#     if "ask_messages" not in st.session_state:
#         st.session_state.ask_messages = [
#             {
#                 "role": "system",
#                 "content": st.session_state.ask_prompt + st.session_state.questions,
#             },
#         ]
#     show_chat(st.session_state.ask_messages)
#     if prompt := st.chat_input("你好，请出题", key="question"):
#         # st.markdown(st.session_state.ask_messages)
#         with st.chat_message("医生"):
#             st.markdown(prompt)
#         st.session_state.ask_messages.append({"role": "user", "content": prompt})
#         with st.spinner("思考中..."):
#             response = chat(
#                 module="zhipu",
#                 modelname="glm-4-flash",
#                 messages=st.session_state.ask_messages,
#             )
#         with st.chat_message("患者"):
#             st.markdown(response)
#         st.session_state.ask_messages.append({"role": "assistant", "content": response})

footer_col_left, footer_col_center, foot_col_save, footer_col_right = st.columns(4)
with footer_col_left:
    if st.button("RERUN", use_container_width=True):
        st.rerun()
# with footer_col_center:
#     if st.button("清除对话", use_container_width=True):
#         for patient in st.session_state.doctor.patients:
#             patient.messages = []

#         del st.session_state.ask_messages
#         st.rerun()
with footer_col_right:
    if st.button("返回首页", use_container_width=True):
        st.switch_page("clinic.py")
# with foot_col_save:
#     if st.button("保存", use_container_width=True):
#         write_prompt(
#             {
#                 "system_prompt": st.session_state.system_prompt,
#                 "ask_prompt": st.session_state.ask_prompt,
#                 "question_prompt": st.session_state.question_prompt,
#                 "questions": st.session_state.questions,
#             }
#         )
#         st.toast("saved...", icon="😍")
