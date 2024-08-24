import random
import uuid
from dataclasses import dataclass, field
from enum import Enum

import pandas as pd
import requests
import streamlit as st
from faker import Faker
from datetime import datetime, timedelta

VOICES = [
    "sambert-zhiwei-v1",
    "sambert-zhijia-v1",
    "sambert-zhiqi-v1",
    "sambert-zhiqian-v1",
    "sambert-zhiru-v1",
    "sambert-zhimiao-emo-v1",
    "sambert-zhifei-v1",
    "sambert-zhigui-v1",
    "sambert-zhijing-v1",
    "sambert-zhilun-v1",
    "sambert-zhimao-v1",
    "sambert-zhina-v1",
    "sambert-zhistella-v1",
    "sambert-zhiting-v1",
    "sambert-zhixiao-v1",
    "sambert-zhiya-v1",
    "sambert-zhiying-v1",
    "sambert-zhiyuan-v1",
    "sambert-zhiyue-v1",
]


class Role(Enum):
    VISITOR = "游客"
    STUDENT = "学生"
    TEACHER = "教师"
    ADMIN = "管理员"

    def __str__(self):
        return self.value


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


@st.cache_data
def read_file(path):
    return pd.read_json(path, orient="records")


def load_questions(server, model, id) -> dict:
    questions_df = read_file(path="data/patients.json")
    questions = questions_df.query(
        f"server == '{server}' & model == '{model}' & id == '{id}'"
    )["questions"].tolist()[0]
    for question in questions:
        random.shuffle(question["answers"])
    return questions


def assign_patients(role, mode) -> list:
    patients_df = read_file(path="data/patients.json")
    match role:
        case _:
            patients_list = patients_df.sample(n=2, ignore_index=True)[
                ["server", "model", "id"]
            ].to_dict(orient="records")
    patients = []
    for patient in patients_list:
        patients.append(Patient(patient["server"], patient["model"], patient["id"]))
    return patients


@dataclass
class Doctor:
    role: Role = Role.VISITOR
    mode: str = None
    id: str = field(default_factory=generate_uuid)
    name: str = None
    grade: str = None
    major: str = None
    patients: list = field(default_factory=list)

    def __post_init__(self):
        self.patients = assign_patients(self.role, self.mode)


@dataclass
class Patient:
    server: str
    model: str
    id: str
    messages: list = field(default_factory=list)
    begin_time: datetime = None
    chat_duration_time: timedelta = timedelta(seconds=0)
    end_time: datetime = None
    inquiry_count: int = 1
    questions: list = field(default_factory=list)

    def __post_init__(self):
        self.questions = load_questions(self.server, self.model, self.id)


@dataclass
class FakeProfile:
    profile: dict = field(default_factory=generate_fake_profile)
    photo: str = field(default_factory=get_random_photo)
    voice: str = field(default_factory=get_random_voice)
