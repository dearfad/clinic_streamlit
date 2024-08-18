import streamlit as st
from libs.bvcpage import set_page_header, show_character_info
from libs.bvcchat import XingChen

set_page_header()

st.session_state.editable = False

def character_info_formatter(x, characters):
    return characters.loc[x, 'name']

st.markdown(":material/admin_panel_settings: **管理员**")

characters = XingChen().characters()
characters = characters.set_index("characterId")

st.write(characters)

index = st.selectbox('选择：', options=characters.index, format_func=lambda x: character_info_formatter(x, characters),)

show_character_info(characters.loc[index].to_dict())



if st.button("返回首页", use_container_width=True):
    st.switch_page("breast.py")
