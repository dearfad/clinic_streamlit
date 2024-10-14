import streamlit as st
from libs.bvcdatabase import (
    read_table,
    read_case,
    update_case_field,
    delete_case,
    update_case_info,
)
import pandas as pd

VIEW_HEIGHT = 450


def page_case_manager():
    cases = read_table(table="case")
    col_case_filter_book, col_case_filter_chapter, col_case_filter_subject = st.columns(3)
    with col_case_filter_book:
        selected_book_unique = list(cases['book'].unique())
        selected_book_unique.insert(0, '任意')
        selected_book = st.selectbox('**教科书**', options=selected_book_unique)
        if selected_book == '任意':
            condition_book = pd.Series([True] * len(cases), index=cases.index)
        else:
            condition_book = (cases['book'] == selected_book)
    with col_case_filter_chapter:
        selected_chapter_unique = list(cases['chapter'].unique())
        selected_chapter_unique.insert(0, '任意')
        selected_chapter = st.selectbox('**章节**', options=selected_chapter_unique)
        if selected_chapter == '任意':
            condition_chapter = pd.Series([True] * len(cases), index=cases.index)
        else:
            condition_chapter = (cases['chapter'] == selected_chapter)
    with col_case_filter_subject:
        selected_subject_unique = list(cases['subject'].unique())
        selected_subject_unique.insert(0, '任意')
        selected_subject = st.selectbox('**主题**', options=selected_subject_unique)
        if selected_subject == '任意':
            condition_subject = pd.Series([True] * len(cases), index=cases.index)
        else:
            condition_subject = (cases['subject'] == selected_subject)
    selected_cases = cases[condition_book & condition_chapter & condition_subject]
    if selected_cases.empty:
        st.warning("没有符合条件的病例")
        st.stop()
    case_dict = st.selectbox(
        label="**病例选择**",
        options=selected_cases.to_dict('records'),
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
            height=VIEW_HEIGHT-58,
            label_visibility="collapsed",
            value=case.content,
            key="case_content",
        )
        col_update_content, col_update_category = st.columns(2)
        with col_update_content:
            if st.button("病历更新", use_container_width=True):
                update_case_field(case.id, field="content", value=case_content)
                st.rerun()
        with col_update_category:
            if st.button("更改信息", use_container_width=True):
                update_case_info(case)

    with tab_case_markdown:
        with st.container(height=VIEW_HEIGHT):
            st.markdown(case_content)
            if case.test:
                st.markdown(case.test)
            if case.story:
                st.markdown(case.story)

    with tab_test_edit:
        test_content = st.text_area(
            "**问题**",
            height=VIEW_HEIGHT-58,
            label_visibility="collapsed",
            value=case.test if case.test else "",
            key='test_content'
        )
        if st.button("问题更新"):
            pass

    with tab_story_edit:
        story_content = st.text_area(
            "**故事**",
            height=VIEW_HEIGHT-58,
            label_visibility="collapsed",
            value=case.story if case.story else "",
            key="story_content"
        )
        if st.button("故事更新"):
            pass

    with tab_case_manager:
        with st.container(height=VIEW_HEIGHT, border=True):
            if st.button("删除病例", type="primary"):
                delete_case(case.id)
                st.rerun()

    col_book, col_chapter, col_subject = st.columns(3)
    with col_book:
        st.caption(f"**教科书**：{case.book}")
    with col_chapter:
        st.caption(f"**章节**：{case.chapter}")
    with col_subject:
        st.caption(f"**主题**：{case.subject}")
