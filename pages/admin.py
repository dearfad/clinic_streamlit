import streamlit as st
from libs.bvcpage import set_page_header
from libs.bvcutils import set_current_user
from libs.bvcdatabase import select_all_model, update_all_model

set_page_header(layout="wide")

with st.expander("模型设定", icon="🚨", expanded=True):
    models = select_all_model()
    modified_models = st.data_editor(
        models,
        num_rows="fixed",
        use_container_width=True,
        column_config={
            "use": st.column_config.CheckboxColumn(
                "使用",
            ),
            "free": st.column_config.CheckboxColumn(
                "免费",
            ),
            "price_input": st.column_config.ProgressColumn(
                "输入价格/千tokens",
                format="%f",
                min_value=0,
                max_value=0.1,
            ),
            "price_output": st.column_config.ProgressColumn(
                "输出价格/千tokens",
                format="%f",
                min_value=0,
                max_value=0.1,
            ),
        },
        height=600,
    )

    if st.button(
        "保存",
        disabled=modified_models.equals(models),
        use_container_width=True,
        type="primary",
    ):
        update_all_model(modified_models)
        st.rerun()

if st.button("退出登录", use_container_width=True, type="primary"):
    set_current_user(st.session_state.cookie_controller, name="游客")
    st.switch_page("clinic.py")

if st.button("返回首页", use_container_width=True):
    st.switch_page("clinic.py")
