from pandas import json_normalize
import streamlit as st
import pandas as pd

models = pd.read_json("data/models.json", )

data = json_normalize(models['series'], meta=[["model"]])

st.write(data)