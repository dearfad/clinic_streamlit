import streamlit as st
from libs.bvcpage import set_page_header, set_page_footer
from libs.bvcdatabase import select_all_model, update_all_model, add_model, delete_model, change_role, add_chapter

set_page_header(layout="wide")

with st.expander("**模型设定**", icon="🚨", expanded=False):
    models = select_all_model()
    modified_models = st.data_editor(
        models,
        num_rows="fixed",
        use_container_width=True,
        hide_index=True,
        disabled=("id",),
        column_config={
            "id": st.column_config.TextColumn(
                "ID",
            ),
            "use": st.column_config.CheckboxColumn(
                "使用",
            ),
            "free": st.column_config.CheckboxColumn(
                "免费",
            ),
            "platform": st.column_config.TextColumn(
                "平台",
            ),
            "series": st.column_config.TextColumn(
                "系列",
            ),
            "name": st.column_config.TextColumn(
                "名称",
            ),
            "module": st.column_config.TextColumn(
                "模块",
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
    col_add, col_update, col_delete = st.columns(3)
    with col_add:
        if st.button(
            ":material/add: **添加**",
            use_container_width=True,
        ):
            add_model()
    with col_update:
        if st.button(
            ":material/update: **更新**",
            disabled=modified_models.equals(models),
            use_container_width=True,
            type="primary",
        ):
            update_all_model(modified_models)
            st.rerun()
    with col_delete:
        if st.button(
            ":material/delete: **删除**",
            use_container_width=True,
        ):
            delete_model(models)

col_user_config, col_chapter_config = st.columns(2)
with col_user_config:
    with st.expander("**用户设定**", icon="🚨", expanded=False):
        if st.button("**更改权限**", use_container_width=True):
            change_role()
with col_chapter_config:
    with st.expander("**章节设定**", icon="🚨", expanded=False):
        if st.button("**添加章节**", use_container_width=True):
            add_chapter()    

set_page_footer()
