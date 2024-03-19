import streamlit as st

st.set_page_config(
    page_title="BreastVSP",
    page_icon="👩",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

st.markdown("<style>div[class^='block-container']{padding-top:2rem;}</style>", unsafe_allow_html=True)
st.subheader("📄 病例分析", divider='rainbow')
st.caption("吉林大学中日联谊医院乳腺外科")
st.write('>**作为一名乳腺外科医生，与患者正在进行沟通，请尝试做出你的诊断。**')

with st.container(border=True):
    col1, col2 = st.columns([1,3], gap='large')
    with col1:
        st.image('dearfad.png')
    with col2:
        st.write('**姓名**：王淑芬')
        st.write('**年龄**：39岁')