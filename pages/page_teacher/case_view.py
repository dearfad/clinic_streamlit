import streamlit as st
from pages.page_libs.case import page_case_manager

def page_case_view():
    
    col_case, col_test, col_background = st.columns(3)
    
    with col_case:
        page_case_manager(page='view')