from libs.models import get_model
# import streamlit as st
model = get_model('tongyi', 'XingChen')
# st.write(model.__name__)
print(model.__name__)