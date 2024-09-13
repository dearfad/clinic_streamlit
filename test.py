import sensenova
import streamlit as st

sensenova.access_key_id = st.secrets['shangtang_access_key_id']
sensenova.secret_access_key = st.secrets['shangtang_secret_access_key']
resp = sensenova.Model.list()
st.write(resp)

