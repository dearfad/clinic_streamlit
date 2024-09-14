import streamlit as st
from libs.bvcpage import set_page_header
from libs.bvcutils import read_models

set_page_header()

st.markdown(":material/admin_panel_settings: **管理员**")

with st.expander("模型设定", icon="🚨"):
    models = read_models()
    modified_models = st.data_editor(models, num_rows="dynamic", use_container_width=True)
    if st.button('保存', disabled=modified_models.equals(models), use_container_width=True, type="primary"):
        modified_models.to_excel('data/models.xlsx', index=False)
        read_models.clear()
        st.rerun()
        
if st.button("返回首页", use_container_width=True):
    st.switch_page("clinic.py")
