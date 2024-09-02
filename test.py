import streamlit as st
import pandas as pd
from libs.bvcutils import read_models

models = read_models()
modified_models = st.data_editor(models)
if st.button('保存'):
    modified_models.to_json('m.json', orient="records", indent=4, force_ascii=False)