import streamlit as st
from libs.bvcpage import set_page_header, show_chat
from libs.bvcutils import read_models, read_prompt, write_prompt
from libs.bvcclasses import Doctor, Role, Patient, Model
from libs.bvcmodels import chat
from datetime import datetime

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


col_system, col_teacher, col_center, col_questions, col_right = st.columns(
    [2, 2, 2, 2, 1]
)
with col_system:
    st.markdown("**SYSTEM_PROMPT**")
    st.text_area(
        "**SYSTEM_PROMPT**",
        value=read_prompt()["system_prompt"],
        key="system_prompt",
        height=280,
        label_visibility="collapsed",
    )
with col_teacher:
    st.markdown("**TEACHER_PROMPT**")
    st.text_area(
        "**TEACHER_PROMPT**",
        value=read_prompt()["teacher_prompt"],
        key="teacher_prompt",
        height=280,
        label_visibility="collapsed",
    )

with col_center:
    st.markdown("**PATIENT_INFO**")
    disease = st.text_input("病种", value="乳房疾病")
    if "patient_info" not in st.session_state:
        st.session_state.patient_info = read_prompt()["patient_info"]
    patient = st.text_area(
        "**PATIENT_INFO**",
        value=st.session_state.patient_info,
        # key="patient_info",
        height=220,
        label_visibility="collapsed",
    )
    if st.button("生成病历", use_container_width=True):
        patient = Patient()
        patient.model = Model(platform="智谱AI", name="glm-4-flash", module="zhipu")
        patient.messages = [
            {
                "role": "system",
                "content": st.session_state.teacher_prompt,
            },
            {"role": "user", "content": disease},
            # {"role": "assistant", "content": "大夫，你好"},
        ]
        response = chat(patient)
        st.session_state.patient_info = response
        st.rerun()

with col_questions:
    st.markdown("**QUESTIONS**")
    if "questions" not in st.session_state:
        st.session_state.questions = read_prompt()["questions"]
    st.text_area(
        "**QUESTIONS**",
        value=st.session_state.questions,
        # key="questions",
        height=220,
        label_visibility="collapsed",
    )
    if st.button("出题", use_container_width=True):
        patient = Patient()
        patient.model = Model(platform="智谱AI", name="glm-4-flash", module="zhipu")
        patient.messages = [
            {
                "role": "system",
                "content": "你是一名外科教师，请根据用户提供病历出3道选择题，按照职业医师考试的形式。在最后给出问题的答案并解析。",
            },
            {"role": "user", "content":  st.session_state.patient_info},
            # {"role": "assistant", "content": "大夫，你好"},
        ]
        response = chat(patient)
        st.session_state.questions = response
        st.rerun()


with col_right:
    st.markdown("**MODELS**")
    models = st.data_editor(
        models_df,
        height=280,
        hide_index=True,
        column_order=("use", "name"),
        use_container_width=True,
    )

selected_models = models[models["use"]]["name"].to_list()
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
    if patient.model.name in selected_models:
        patient.model.use = True
    else:
        patient.model.use = False

    if patient.model.use:
        with st.session_state.chat_container[patient.model.name]:
            show_chat(patient.messages)

cols = st.columns(3)
with cols[1]:
    chat_input_placeholder = st.container()
    if prompt := chat_input_placeholder.chat_input(""):
        for patient in st.session_state.doctor.patients:
            if patient.model.use:
                with st.session_state.chat_container[patient.model.name]:
                    with st.chat_message("医生"):
                        st.markdown(prompt)
                    patient.messages.append({"role": "user", "content": prompt})
                    start_time = datetime.now()
                    with st.spinner("思考中..."):
                        response = chat(patient)
                    st.markdown(
                        f":stopwatch: {round((datetime.now()-start_time).total_seconds(),2)} 秒"
                    )
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
        st.switch_page("clinic.py")
with foot_col_save:
    if st.button("保存", use_container_width=True):
        write_prompt(
            {
                "system_prompt": st.session_state.system_prompt,
                "teacher_prompt": st.session_state.teacher_prompt,
                "patient_info": st.session_state.patient_info,
                "questions": st.session_state.questions,
            }
        )
        st.toast("saved...", icon="😍")
