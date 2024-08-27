import streamlit as st
import pandas as pd
import pickle
import os


CHAPTER = {
    "乳房疾病": "breast",
}


@st.cache_data
def read_file(path):
    return pd.read_json(path, orient="records")


def reset_session_state():
    for key in st.session_state.keys():
        if key != "voice":
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


