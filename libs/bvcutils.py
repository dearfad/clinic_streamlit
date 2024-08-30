import os
import pickle
import random
import uuid

import pandas as pd
import requests
import streamlit as st
from faker import Faker

from libs.bvcconst import VOICES


@st.cache_data
def read_file(path):
    return pd.read_json(path, orient="records")


def reset_session_state(exclude=["voice"]):
    for key in st.session_state.keys():
        if key not in exclude:
            del st.session_state[key]


def save_data():
    if not os.path.exists("data/doctors.pkl"):
        doctors = [st.session_state.doctor]
        with open("data/doctors.pkl", "wb") as file:
            pickle.dump(doctors, file)
    else:
        with open("data/doctors.pkl", "rb") as file:
            doctors = pickle.load(file)
        doctors.append(st.session_state.doctor)
        with open("data/doctors.pkl", "wb") as file:
            pickle.dump(doctors, file)


def load_data():
    with open("data/doctors.pkl", "rb") as file:
        doctors = pickle.load(file)
    return doctors


def user_info_formatter(user):
    match user.role:
        case "游客":
            return str(f"{user.name} - {user.chatlog.loc[0, "start_time"]}")

        case "学生":
            return str(
                f"{user.name} - {user.chatlog.loc[0, "start_time"]} - {user.grade}级 - {user.major}专业"
            )


def fix_img_tts(response):
    return response.split("![]")[0].strip()


def get_patient_info(patient):
    info_df = read_file("data/patients.json")
    infos = info_df.query(
        f"server == '{patient.server}' & model == '{patient.model}' & id == '{patient.id}'"
    )["info"].tolist()[0]
    info = ""
    for key, value in infos.items():
        info = info + f"{key}：{value}" + "\n"
    return info


def generate_uuid() -> str:
    return str(uuid.uuid4())


def generate_fake_profile():
    return Faker("zh_CN").profile(sex="F")


def get_random_photo() -> str:
    imagehost = random.choice(
        [
            "https://cdn.seovx.com/?mom=302",
            "https://cdn.seovx.com/d/?mom=302",
            "https://cdn.seovx.com/ha/?mom=302",
        ]
    )
    response = requests.get(imagehost, allow_redirects=False)
    if response.status_code == 302:
        return "https:" + response.headers.get("Location")
    else:
        return "https://api.multiavatar.com/" + str(uuid.uuid4()) + ".png"


def get_random_voice() -> str:
    return random.choice(VOICES)
