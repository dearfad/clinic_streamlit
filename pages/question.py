import streamlit as st
from datetime import datetime
from libs.bvcpage import set_page_header, show_setting_page, show_chat
from libs.bvcutils import save_data

set_page_header()
show_setting_page()

id = st.session_state.id
doctor = st.session_state.doctor
patient = doctor.patients[id]

st.markdown(f"**就诊编号: {id+1} / {len(doctor.patients)}**")

with st.expander(label=":page_facing_up: **对话记录**"):
    st.markdown(f"**:repeat: {patient.inquiry_count}**")
    show_chat(patient.messages)

for index, question in enumerate(patient.questions):
    key = "a" + str(index)
    st.radio(f"**Q{index+1}: {question['question']}**", question["answers"], key=key)

if st.button("再问一下", use_container_width=True):
    patient.inquiry_count += 1
    st.switch_page("pages/inquiry.py")

if st.button("提交答案", use_container_width=True):
    patient.end_time = datetime.now()
    for a in range(len(patient.questions)):
        k = "a" + str(a)
        patient.questions[a]["answer"] = st.session_state[k]
    st.session_state.id += 1
    if st.session_state.id == len(doctor.patients):
        st.write(doctor)
        save_data()
        st.switch_page("pages/result.py")
    else:
        del st.session_state.fakeprofile
        st.switch_page("pages/inquiry.py")
