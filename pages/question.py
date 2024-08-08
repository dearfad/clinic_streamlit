import streamlit as st
from datetime import datetime
from libs.bvcpage import set_page_header, show_chat
from libs.bvcutils import save_data

set_page_header()

user = st.session_state.user

st.markdown(f"**就诊编号: {user.index+1} / {len(user.chatlog)}**")

with st.expander(label=":page_facing_up: **对话记录**"):
    st.markdown(f"**:repeat: {user.chatlog.loc[user.index, 'inquiry_count']}**")
    show_chat(st.session_state.messages)

case_question = user.chatlog.loc[user.index, "questions"]

for index, question in enumerate(case_question):
    key = "a" + str(index)
    st.radio(
        f"**Q{index+1}: {question['question']}**", question["answer_list"], key=key
    )

if st.button("再问一下", use_container_width=True):
    user.chatlog.loc[user.index, "inquiry_count"] += 1
    st.switch_page('pages/inquiry.py')

if st.button("提交答案", use_container_width=True):
    user.chatlog.loc[user.index, "end_time"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    for a in range(len(case_question)):
        k = "a" + str(a)
        case_question[a]["user_answer"] = st.session_state[k]
    user.index += 1
    if user.index == len(user.chatlog):
        save_data()
        st.switch_page("pages/result.py")
    else:
        del st.session_state.messages
        del st.session_state.patient
        st.switch_page("pages/inquiry.py")
