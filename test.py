import streamlit as st
from libs.bvcutils import get_models

models = get_models()

st.write(models)
