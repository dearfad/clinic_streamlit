from datetime import datetime

import streamlit as st

from libs.bvcchat import chat
from libs.bvcclass import Patient
from libs.bvcpage import set_page_header, show_chat
from libs.bvctts import tts
from libs.bvcutils import fix_img_tts

set_page_header()

settings_expander = st.expander("**设置**", icon=":material/settings:")

with settings_expander:
    col_left, col_right = st.columns(2)
    with col_left:
        if "voice" not in st.session_state:
            st.session_state.voice = False
        voice = st.toggle("**语音输出**", value=st.session_state.voice)
        st.session_state.voice = True if voice else False
    with col_right:
        if st.button("返回首页"):
            st.switch_page("breast.py")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "大夫，你好"},
    ]

if "patient" not in st.session_state:
    st.session_state.patient = Patient()

user = st.session_state.user


patient = st.session_state.patient
character_id = user.chatlog.loc[user.index, "id"]
st.markdown(f"**就诊编号: {user.index+1} / {len(user.chatlog)}**")

with st.container(border=False):
    col_left, col_right = st.columns([1, 3])
    with col_left:
        st.image(patient.photo, use_column_width=True)
    with col_right:
        with st.container(border=True):
            st.markdown(f"姓名: **{patient.profile['name']}**")
            st.markdown(f"地址: **{patient.profile['address']}**")
            st.markdown(f"单位: **{patient.profile['company']}**")
            st.markdown(f"职位: **{patient.profile['job']}**")

st.markdown(":page_facing_up: **谈话记录**")
show_chat(st.session_state.messages)
# 如果再次询问，不重新记录开始时间
if user.chatlog.loc[user.index, "start_time"] == "":
    user.chatlog.loc[user.index, "start_time"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

if prompt := st.chat_input(""):
    if prompt != "我问完了":
        with st.chat_message("医"):
            st.write(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("患"):
            response = chat(
                role_server="xingchen",
                character_id=character_id,
                messages=st.session_state.messages,
            )
            st.markdown(f"**{response}**")
            st.session_state.messages.append({"role": "assistant", "content": response})
            if st.session_state.voice:
                settings_expander.audio(
                    tts(
                        text=fix_img_tts(response), model=st.session_state.patient.voice
                    ),
                    autoplay=True,
                )  # TTS
    else:
        user.chatlog.loc[user.index, "conversation_end_time"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        st.session_state.messages.append({"role": "user", "content": prompt})
        user.chatlog.loc[user.index, "messages"] = str(st.session_state.messages)
        st.switch_page("pages/question.py")
