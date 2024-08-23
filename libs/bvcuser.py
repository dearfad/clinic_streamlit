from dataclasses import dataclass, field
from enum import Enum
import uuid
from faker import Faker

import random
import requests



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
    response = requests.get("https://cdn.seovx.com/?mom=302", allow_redirects=False)
    print(response.status_code)
    if response.status_code == 302:
        return "https:" + response.headers.get("Location")
    else:
        return "https://api.multiavatar.com/" + str(uuid.uuid4()) + ".png"

def get_random_voice() -> str:
    return random.choice(VOICES)


@dataclass
class Doctor:
    role: Role = Role.VISITOR
    mode: str = None
    id: str = field(default_factory=generate_uuid)
    name: str = None
    grade: str = None
    major: str = None
    logs: list = field(default_factory=list)


@dataclass
class Patient:
    server: str
    model: str
    id: str
    profile: dict = field(default_factory=generate_fake_profile)
    photo: str = field(default_factory=get_random_photo)
    voice: str = field(default_factory=get_random_voice)

patient = Patient(server='test', model='test', id='test')
print(patient)

# import pandas as pd



# from libs.bvcutils import read_cases, get_random_photo

#     def create_chatlog(self):
#         data = read_cases("cases/breast_case.json")
#         match self.role:
#             case "游客":
#                 data = data.sample(n=1, ignore_index=True)
#             case "学生":
#                 data = data.sample(frac=1, ignore_index=True)
#         for questions in data["questions"]:
#             for question in questions:
#                 random.shuffle(question["answer_list"])

#         self.chatlog = pd.DataFrame(data)
#         self.chatlog["start_time"] = ""
#         self.chatlog["conversation_end_time"] = ""
#         self.chatlog["end_time"] = ""
#         self.chatlog["messages"] = ""
#         self.chatlog["inquiry_count"] = 1
