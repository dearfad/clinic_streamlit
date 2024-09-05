import streamlit as st
from libs.bvcpage import set_page_header, show_chat
from libs.bvcutils import read_models, read_prompt, write_prompt
from libs.bvcclasses import Doctor, Role
from libs.bvcmodels import chat

set_page_header(layout="wide")

st.markdown("#### 模型研究")

models_df = read_models()

if "doctor" not in st.session_state:
    st.session_state.doctor = Doctor(role=Role.TEACHER, mode="模型研究")
    st.session_state.doctor.assign_patients()
else:
    st.session_state.doctor.mode = "模型研究"
    if not st.session_state.doctor.patients:
        st.session_state.doctor.assign_patients()
if "chat_container" not in st.session_state:
    st.session_state.chat_container = {}


col_left, col_center, col_right = st.columns(3)
with col_left:
    st.markdown("**SYSTEM_PROMPT**")
    st.text_area(
        "**SYSTEM_PROMPT**",
        value=read_prompt()['system_prompt'],
        key="system_prompt",
        height=280,
        label_visibility="collapsed",
    )

with col_center:
    st.markdown("**PATIENT_INFO**")
    st.text_area(
        "**PATIENT_INFO**",
        value=read_prompt()['patient_info'],
        key="patient_info",
        height=280,
        label_visibility="collapsed",
    )
with col_right:
    st.markdown("**MODELS**")
    models = st.data_editor(
        models_df,
        height=280,
        hide_index=True,
        column_order=("use", "platform", "model"),
        use_container_width=True,
    )

selected_models = models[models["use"]]["model"].to_list()
if len(selected_models) == 0:
    st.warning("请至少选择一个模型...")
    st.stop()

chat_cols = st.columns(len(selected_models))
for i, col in enumerate(chat_cols):
    with col:
        st.session_state.chat_container[selected_models[i]] = st.container(
            height=210, border=True
        )
        st.markdown(f"**{selected_models[i]}**")

for patient in st.session_state.doctor.patients:
    patient.info = st.session_state.patient_info
    if not patient.messages:
        patient.messages = [
            {
                "role": "system",
                "content": st.session_state.system_prompt + patient.info,
            },
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "大夫，你好"},
        ]
    if patient.model.model in selected_models:
        patient.model.use = True
    else:
        patient.model.use = False

    if patient.model.use:
        with st.session_state.chat_container[patient.model.model]:
            show_chat(patient.messages)

cols = st.columns(3)
with cols[1]:
    chat_input_placeholder = st.container()
    if prompt := chat_input_placeholder.chat_input(""):
        for patient in st.session_state.doctor.patients:
            if patient.model.use:
                with st.session_state.chat_container[patient.model.model]:
                    with st.chat_message("医生"):
                        st.markdown(prompt)
                    patient.messages.append({"role": "user", "content": prompt})
                    with st.spinner("思考中..."):
                        response = chat(st.session_state.doctor, patient)
                    with st.chat_message("患者"):
                        st.markdown(response)
                    patient.messages.append({"role": "assistant", "content": response})

footer_col_left, footer_col_center, foot_col_save, footer_col_right = st.columns(4)
with footer_col_left:
    if st.button("RERUN", use_container_width=True):
        st.rerun()
with footer_col_center:
    if st.button("清除对话", use_container_width=True):
        for patient in st.session_state.doctor.patients:
            patient.messages = []
        st.rerun()
with footer_col_right:
    if st.button("返回首页", use_container_width=True):
        st.switch_page("bvc.py")
with foot_col_save:
    if st.button('保存', use_container_width=True):
        write_prompt({
                "system_prompt": st.session_state.system_prompt,
                "patient_info": st.session_state.patient_info
            })
        st.toast("saved...", icon='😍')
