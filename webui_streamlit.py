import streamlit as st

st.set_page_config(
    page_title="BreastVSP",
    page_icon="👩",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", unsafe_allow_html=True)

st.header("👩 病例分析", divider='red')
st.caption("吉林大学中日联谊医院乳腺外科")
st.write('**你是一名乳腺外科医生，现在用平常谈话的方法跟眼前的患者沟通，请尝试做出你的诊断。**')