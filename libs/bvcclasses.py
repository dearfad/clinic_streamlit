import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

from libs.bvcutils import (
    generate_fake_profile,
    generate_uuid,
    get_random_photo,
    get_random_voice,
    read_file,
)


class Role(Enum):
    VISITOR = "游客"
    STUDENT = "学生"
    TEACHER = "教师"
    ADMIN = "管理员"

    def __str__(self):
        return self.value

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
            patients_list = patients_df.sample(n=1, ignore_index=True)[
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
    platform: str
    series: str
    name: str
    model: str
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
