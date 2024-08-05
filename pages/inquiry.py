import streamlit as st
from datetime import datetime
from libs.bvcpage import set_page_header, show_chat
from libs.bvcchat import chat

set_page_header()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "大夫，你好"},
    ]


user = st.session_state.user
character_id = user.chatlog.loc[user.index, "id"]
st.markdown(f"**就诊编号: {user.index+1} / {len(user.chatlog)}**")
st.markdown(f"**:date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}**")
st.markdown(":page_facing_up: **谈话记录**")
# col_left, col_center, col_right = st.columns([1, 3, 1])
# with col_center:
#     st.caption(
#         f"患者编号：**{user.index+1} / {len(user.chatlog)}**")
#     st.image(
#         "https://cdn.seovx.com/d/?mom=302",
#         caption=st.session_state.faker.name(),
#         use_column_width=True,
#     )
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
    else:
        user.chatlog.loc[user.index, "conversation_end_time"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        st.session_state.messages.append({"role": "user", "content": prompt})
        user.chatlog.loc[user.index, "messages"] = str(st.session_state.messages)
        st.switch_page('pages/question.py')
