import streamlit as st

from libs.bvcclasses import Doctor, Patient, assign_patients, Role

patients = assign_patients(Role.VISITOR, None)

st.write(patients[0])
