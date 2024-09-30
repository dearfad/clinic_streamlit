import streamlit as st

from libs.bvcpage import set_page_header, set_page_footer
from pages.page_teacher.case_generate import page_case_generate
from pages.page_teacher.test_generate import page_test_generate

set_page_header(layout="wide")

st.markdown("##### :material/view_headline: 模型研究 :material/view_headline:")

tab_case_generate, tab_question_generate, tab_patient, tab_ask = st.tabs(
    ["病例生成", "问题生成", "病例问诊", "问答分析"]
)

with tab_case_generate:
    page_case_generate()


with tab_question_generate:
    page_test_generate()

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

# footer_col_left, footer_col_center, foot_col_save, footer_col_right = st.columns(4)
# with footer_col_left:
#     if st.button("RERUN", use_container_width=True):
#         st.rerun()
# with footer_col_center:
#     if st.button("清除对话", use_container_width=True):
#         for patient in st.session_state.doctor.patients:
#             patient.messages = []

#         del st.session_state.ask_messages
#         st.rerun()
# with footer_col_right:
#     if st.button("返回首页", use_container_width=True):
#         st.switch_page("clinic.py")
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


set_page_footer()
