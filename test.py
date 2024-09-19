import sqlite3
import pandas as pd
import streamlit as st

connect = sqlite3.connect('data/clinic.db')
with connect:
    models_df = pd.read_sql("SELECT name, module FROM models WHERE use=True", con=connect)

models = models_df.to_dict(orient='records')
m = st.selectbox('model', models, format_func=lambda x:x['name'])
st.write(m)
