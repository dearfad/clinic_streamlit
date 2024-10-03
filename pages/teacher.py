import streamlit as st

from libs.bvcpage import set_page_header, set_page_footer
from pages.page_teacher.case_generate import page_case_generate
from pages.page_teacher.test_generate import page_test_generate
from pages.page_teacher.sim_patient import page_sim_patient
from pages.page_teacher.ask_answer import page_ask_answer

set_page_header(layout="wide")

st.markdown("##### :material/view_headline: 模型研究 :material/view_headline:")


tab_case_generate, tab_question_generate, tab_sim_patient, tab_ask_answer = st.tabs(
    ["病例生成", "问题生成", "病例问诊", "问答分析"]
)

with tab_case_generate:
    page_case_generate()


with tab_question_generate:
    page_test_generate()

with tab_sim_patient:
    page_sim_patient()

with tab_ask_answer:
    page_ask_answer()




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




set_page_footer()

st.session_state.info_placeholder = st.empty()