import importlib
import random

import streamlit as st

from libs.bvcclasses import Doctor, Patient


def get_model(patient):
    api_key = random.choice(st.secrets[patient.model.apikey])
    platform = importlib.import_module(f"libs.platforms.{patient.model.module}")
    ModelClass = getattr(platform, patient.model.classname)
    model = ModelClass(api_key=api_key)
    return model


def chat(doctor: Doctor, patient: Patient):
    model = get_model(patient)
    response = model.chat(doctor, patient)
    return response
