from datetime import datetime

import streamlit as st

from libs.bvcclasses import FakeProfile
from libs.bvcmodels import chat
from libs.bvcpage import set_page_header, show_chat, show_setting_page
from libs.bvctts import tts
from libs.bvcutils import fix_img_tts
from libs.bvcconst import CHAT_OPENING

set_page_header()

show_setting_page()

voice_placeholder = st.container(height=1, border=False)

# 就诊患者顺序
if "id" not in st.session_state:
    st.session_state.seqid = 0
if "fakeprofile" not in st.session_state:
    st.session_state.fakeprofile = FakeProfile()

# 设置进入页面时间
if "current_begin_time" not in st.session_state:
    st.session_state.current_begin_time = datetime.now()

# 缩写，请勿赋值
seqid = st.session_state.seqid
doctor = st.session_state.doctor
fakeprofile = st.session_state.fakeprofile
patient = doctor.patients[seqid]

# # 如果再次询问，不重新记录开始时间
if patient.begin_time is None:
    patient.begin_time = datetime.now()

if patient.messages == []:
    patient.messages = CHAT_OPENING

st.markdown(f"**就诊编号: {seqid+1} / {len(doctor.patients)}**")
with st.container(border=False):
    col_left, col_right = st.columns([2, 3])
    with col_left:
        st.image(fakeprofile.photo, use_column_width=True)
        # model_dict = {"xingchen": "星辰", "qwen": "千问", "glm": "智谱"}
        # st.caption(f"**🆔 :red-background[{model_dict[patient.model]}]**")
    with col_right:
        with st.container(border=True):
            st.markdown(f"姓名: **{fakeprofile.profile['name']}**")
            st.markdown(f"地址: **{fakeprofile.profile['address']}**")
            st.markdown(f"单位: **{fakeprofile.profile['company']}**")
            st.markdown(f"职位: **{fakeprofile.profile['job']}**")

st.markdown(":page_facing_up: **谈话记录**")


show_chat(patient.messages)
if prompt := st.chat_input(""):
    if prompt != "我问完了":
        with st.chat_message("医生"):
            st.markdown(prompt)
        with st.spinner("思考中..."):
            response = chat(doctor=doctor, patient=patient)
        with st.chat_message("患者"):
            st.markdown(response)

        patient.messages.append({"role": "user", "content": prompt})
        patient.messages.append({"role": "assistant", "content": response})

        # TTS
        if st.session_state.voice:
            voice_placeholder.audio(
                tts(text=fix_img_tts(response), model=fakeprofile.voice),
                autoplay=True,
            )

    else:
        patient.chat_duration_time += (
            datetime.now() - st.session_state.current_begin_time
        )
        del st.session_state.current_begin_time
        patient.messages.append({"role": "user", "content": prompt})
        st.switch_page("pages/question.py")
