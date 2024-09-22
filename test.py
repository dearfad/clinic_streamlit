from streamlit_cookies_controller import CookieController
import streamlit as st

cookie_controller = CookieController()
# cookie_controller.remove('user')
st.write(cookie_controller.getAll())