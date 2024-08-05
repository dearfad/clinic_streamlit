import streamlit as st
import pickle
from libs.bvcutils import set_page_header, user_info_formatter, load_data


# set_page_header()

# chapter = st.selectbox("**章节**",("乳房疾病",))

# mode = st.selectbox("**模式**", ("记录浏览", "理论授课", "教学研究"))

users = load_data()
st.write('ok')

# st.selectbox(
#         "**用户**",
#         users,
#         format_func=lambda x: user_info_formatter(x),
#         key="user",
#     )

# # show_result()

# if st.button("返回首页", use_container_width=True):
#     st.switch_page("breast.py")