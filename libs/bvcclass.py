import random
import pandas as pd
from faker import Faker
from libs.bvcutils import read_cases, get_random_photo
import uuid


class User:
    def __init__(self, role, chapter, name, grade, major, mode):
        self.role = role
        self.chapter = chapter  # 乳房疾病
        self.name = name
        self.grade = grade
        self.major = major
        self.mode = mode
        self.index = 0
        self.id = uuid.uuid4()
        self.chatlog: pd.DataFrame

    def create_chatlog(self):
        data = read_cases("cases/breast_case.json")
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
        faker = Faker("zh_CN")
        self.profile = faker.profile(sex="F")
        self.photo = get_random_photo(seed=self.profile["name"])
        self.voice = random.choice(
            [
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
        )
