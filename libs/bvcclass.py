import random

import pandas as pd
import streamlit as st
from faker import Faker
import requests

from libs.bvcutils import read_cases


class User:
    def __init__(self, role, chapter, name, grade, major, mode):
        self.role = role
        self.chapter = chapter # 乳房疾病
        self.name = name
        self.grade = grade
        self.major = major
        self.mode = mode
        self.index = 0
        self.chatlog: pd.DataFrame

    def create_chatlog(self):
        data = read_cases("cases/breast.json")
        match self.role:
            case "游客":
                data = data.sample(n=1, ignore_index=True)
            case "学生":
                data = data.sample(frac=1, ignore_index=True)
        for questions in data["questions"]:
            for question in questions:
                random.shuffle(question["answer_list"])

        self.chatlog = pd.DataFrame(data)
        self.chatlog["start_time"] = ""
        self.chatlog["conversation_end_time"] = ""
        self.chatlog["end_time"] = ""
        self.chatlog["messages"] = ""
        self.chatlog["inquiry_count"] = 1

class Patient:
    def __init__(self):
        faker = Faker('zh_CN')
        self.profile = faker.profile(sex="F")
        self.photo = requests.get("https://cdn.seovx.com/?mom=302").url