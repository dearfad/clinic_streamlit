import importlib
import random

import streamlit as st

from libs.bvcclasses import Doctor, Patient


MODEL_CLASS = {
    "xingchen": "XingChen",
    "baichuan": "BaiChuan",
    "qwen": "Qwen",
}


def get_model(server_name: str, model_name: str, api_key: str):
    server = importlib.import_module(f"libs.servers.{server_name}")
    ModelClass = getattr(server, MODEL_CLASS[model_name])
    model = ModelClass(api_key=api_key)
    return model


def chat(doctor: Doctor, patient: Patient):
    api_key = random.choice(st.secrets[patient.model])
    model = get_model(patient.server, patient.model, api_key)
    response = model.chat(doctor, patient)
    return response
