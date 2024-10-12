import streamlit as st
from libs.bvcdatabase import (
    read_category_field_distinct,
    read_table,
    read_case_category,
)



def page_case_manager(page):
    cases = read_table(table='case').to_dict(orient="records")
    case_dict = st.selectbox(
        label="**病例选择**",
        options=cases,
        format_func=lambda x: f"{x['profile']} == {x['creator']}",
        key=f"{page}_case_dict",
    )

    tab_case_markdown, tab_case_textarea, tab_case_manager = st.tabs(
        ["查看", "编辑", "管理"]
    )
    with tab_case_textarea:
        case_content = st.text_area(
            "**病例**",
            height=408,
            label_visibility="collapsed",
            value=case_dict['content'],
            key=f"{page}_case_content",
        )
    with tab_case_markdown:
        with st.container(height=410):
            st.markdown(case_content)
    with tab_case_manager:
        with st.container(height=410, border=True):
            cols = st.columns(3)
            with cols[0]:
                book = st.selectbox("**教科书**", read_category_field_distinct("book"), key=f"{page}_book")
            with cols[1]:
                chapter = st.selectbox("**章节**", read_category_field_distinct("chapter"), key=f"{page}_chapter")
            with cols[2]:
                subject = st.selectbox("**主题**", read_category_field_distinct("subject"), key=f"{page}_subject")

    col_book, col_chapter, col_subject = st.columns(3)
    category = read_case_category(case_dict['id'])
    with col_book:
        st.caption(f"**教科书**：{category.book}")
    with col_chapter:
        st.caption(f"**章节**：{category.chapter}")
    with col_subject:
        st.caption(f"**主题**：{category.subject}")
    