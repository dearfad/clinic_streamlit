import streamlit as st
from libs.bvcdatabase import (
    read_table,
    read_case,
    update_case,
    delete_case,
    update_case_category,
)

HEIGHT = 450


def page_case_manager():
    cases = read_table(table="case").to_dict(orient="records")

    case_dict = st.selectbox(
        label="**病例选择**",
        options=cases,
        format_func=lambda x: f"{x['profile']} == {x['creator']}",
        key="case",
    )
    case = read_case(case_dict["id"])

    (
        tab_case_markdown,
        tab_case_edit,
        tab_test_edit,
        tab_story_edit,
        tab_case_manager,
    ) = st.tabs(["查看", "病历编辑", "问题编辑", "故事编辑", "管理"])

    with tab_case_edit:
        case_content = st.text_area(
            "**病例**",
            height=HEIGHT-58,
            label_visibility="collapsed",
            value=case.content,
        )
        col_update_content, col_update_category = st.columns(2)
        with col_update_content:
            if st.button("病历更新", use_container_width=True):
                update_case(case.id, field="content", value=case_content)
                st.rerun()
        with col_update_category:
            if st.button("更改类别", use_container_width=True):
                update_case_category(case.id)

    with tab_case_markdown:
        with st.container(height=HEIGHT):
            st.markdown(case_content)
            if case.test:
                st.markdown(case.test.content)

    with tab_test_edit:
        test_content = st.text_area(
            "**问题**",
            height=HEIGHT-58,
            label_visibility="collapsed",
            value=case.test.content if case.test else "",
        )
        if st.button("问题更新"):
            pass
    with tab_story_edit:
        story_content = st.text_area(
            "**故事**",
            height=HEIGHT-58,
            label_visibility="collapsed",
            # value=case.content,
        )
        if st.button("故事更新"):
            pass
    with tab_case_manager:
        with st.container(height=HEIGHT, border=True):
            if st.button("删除病例", type="primary"):
                delete_case(case.id)
                st.rerun()

    col_book, col_chapter, col_subject = st.columns(3)
    with col_book:
        st.caption(f"**教科书**：{case.category.book}")
    with col_chapter:
        st.caption(f"**章节**：{case.category.chapter}")
    with col_subject:
        st.caption(f"**主题**：{case.category.subject}")
