import os
import pickle
import random
import uuid


import pandas as pd
import requests
import streamlit as st
from faker import Faker
import json
from libs.bvcconst import VOICES, SYSTEM_PROMPT


@st.cache_data
def read_patients():
    return pd.read_json("data/patients.json", orient="records")


@st.cache_data
def read_models():
    with open("data/models.json", "r", encoding="utf-8") as file:
        return json.load(file)


def get_models():
    models_json = read_models()
    models_df = pd.json_normalize(
        models_json, ["info", "models"], ["platform", "api", ["info", "series"]]
    )
    models_all = models_df.rename(columns={"info.series": "series"})[
        ["platform", "series", "name", "model", "price", "api", "use"]
    ]
    return models_all[models_all["use"]].reset_index(drop=True).drop('use', axis=1)


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
    info = ""
    for key, value in patient.info.items():
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


def build_system_prompt(patient):
    info = get_patient_info(patient)
    content = SYSTEM_PROMPT + info
    system_prompt = [{"role": "system", "content": content}]
    print(system_prompt[0]['content'])
    return system_prompt