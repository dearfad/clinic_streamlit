from datetime import datetime

import streamlit as st

from libs.bvcclasses import FakeProfile
from libs.bvcmodels import chat
from libs.bvcpage import set_page_header, show_chat
from libs.bvctts import tts
from libs.bvcutils import fix_img_tts, reset_session_state

set_page_header()

if "doctor" not in st.session_state:
    st.switch_page('bvc.py')

doctor = st.session_state.doctor

if "id" not in st.session_state:
    st.session_state.id = 0
id = st.session_state.id

if "fakeprofile" not in st.session_state:
    st.session_state.fakeprofile = FakeProfile()
fakeprofile = st.session_state.fakeprofile

patient = doctor.patients[id]


col_left, col_right = st.columns(2)
with col_left:
    if st.button("返回首页"):
        reset_session_state()
        st.switch_page("bvc.py")
with col_right:
    if "voice" not in st.session_state:
        st.session_state.voice = False
    setting_popover = st.popover(":material/settings:**设置**")
    with setting_popover:
        voice = st.toggle("**语音输出**", value=st.session_state.voice)
        st.session_state.voice = True if voice else False

if patient.messages == []:
    patient.messages = [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "大夫，你好"},
    ]

st.markdown(f"**就诊编号: {id+1} / {len(doctor.patients)}**")
with st.container(border=False):
    col_left, col_right = st.columns([2, 3])
    with col_left:
        st.image(fakeprofile.photo, use_column_width=True)
        model_dict = {"xingchen": "星辰"}
        st.caption(f"**🆔 :red-background[{model_dict[patient.model]}]**")
    with col_right:
        with st.container(border=True):
            st.markdown(f"姓名: **{fakeprofile.profile['name']}**")
            st.markdown(f"地址: **{fakeprofile.profile['address']}**")
            st.markdown(f"单位: **{fakeprofile.profile['company']}**")
            st.markdown(f"职位: **{fakeprofile.profile['job']}**")

st.markdown(":page_facing_up: **谈话记录**")

st.write(patient.chat_duration_time)

show_chat(patient.messages)

# # 如果再次询问，不重新记录开始时间
if patient.begin_time is None:
    patient.begin_time = datetime.now()

if "current_begin_time" not in st.session_state:
    st.session_state.current_begin_time = datetime.now()

if prompt := st.chat_input(""):
    if prompt != "我问完了":
        with st.chat_message("医"):
            st.write(prompt)
            patient.messages.append({"role": "user", "content": prompt})
        with st.chat_message("患"):
            response = chat(
                doctor=doctor,
                patient=patient,
            )
            st.markdown(f"**{response}**")
            patient.messages.append({"role": "assistant", "content": response})
            if st.session_state.voice:
                setting_popover.audio(
                    tts(text=fix_img_tts(response), model=fakeprofile.voice),
                    autoplay=True,
                )  # TTS
    else:
        patient.chat_duration_time += (
            datetime.now() - st.session_state.current_begin_time
        )
        del st.session_state.current_begin_time
        patient.messages.append({"role": "user", "content": prompt})
        st.switch_page("pages/question.py")
