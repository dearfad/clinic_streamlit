import streamlit as st

import pandas as pd

df = pd.read_json('cases/breast.json', orient='records')


sample = df.sample(frac=1)

