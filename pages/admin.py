import streamlit as st
from libs.bvcpage import set_page_header, show_character_info
from libs.models import XingChen

set_page_header()

st.markdown(":material/admin_panel_settings: **管理员**")

characters = XingChen().characters()

characterId = st.selectbox('选择：', options=characters['characterId'], format_func=lambda x: characters.loc[characters['characterId']==x, 'name'].values[0])

character = characters.loc[characters['characterId']==characterId].to_dict(orient='records')[0]

show_character_info(character)

if st.button("返回首页", use_container_width=True):
    st.switch_page("breast.py")
