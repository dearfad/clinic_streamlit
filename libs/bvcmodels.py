import importlib
import random

import streamlit as st

from libs.bvcclasses import Doctor, Patient


MODEL_CLASS = {
    "阿里云百炼": "BaiLian",
    "智谱AI": "ZhiPu",
}

PLATFORM = {
    '阿里云百炼': 'bailian',
    '智谱AI': 'zhipu',
}

def get_model(patient):
    api_key = random.choice(st.secrets[patient.api])
    platform = importlib.import_module(f"libs.platforms.{PLATFORM[patient.platform]}")
    ModelClass = getattr(platform, MODEL_CLASS[patient.platform])
    model = ModelClass(api_key=api_key)
    return model


def chat(doctor: Doctor, patient: Patient):
    model = get_model(patient)
    response = model.chat(doctor, patient)
    return response
