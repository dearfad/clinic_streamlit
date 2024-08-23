import streamlit as st
from libs.bvcuser import Doctor, Patient, FakeProfile

user = Doctor()
st.write(user)

patient = Patient("tongyi", "xingchen", "37d0bb98a0194eefbecdba794fb1b42c")
st.write(patient)
st.write(patient.questions)

fakeprofile = FakeProfile()
st.write(fakeprofile)
