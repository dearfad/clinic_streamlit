import sqlite3

import pandas as pd
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column
from sqlalchemy import Integer, Text, Float, text

engine = create_engine("sqlite:///data/clinic.db")
Session = sessionmaker(bind=engine)


def connect_db():
    return sqlite3.connect("data/clinic.db")


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)


class Model(Base):
    __tablename__ = "models"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    use: Mapped[bool] = mapped_column(nullable=False)
    free: Mapped[bool] = mapped_column(nullable=False)
    platform: Mapped[str] = mapped_column(nullable=False)
    series: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=True)
    module: Mapped[str] = mapped_column(nullable=True)
    print_input: Mapped[float] = mapped_column(nullable=True)
    print_output: Mapped[float] = mapped_column(nullable=True)


def create_all_table():
    Base.metadata.create_all(engine)


def user_register(username, password):
    with Session() as session:
        user = User(name=username, password=password)
        session.add(user)
        session.commit()


def check_user_exist(username):
    with Session() as session:
        result = session.execute(select(User).where(User.name == username))
        user = result.scalar_one()
    return True if user else False


def user_login(username, password):
    with Session() as session:
        result = session.execute(select(User).where(User.name == username))
        user = result.scalar_one()
    return True if user and user.password == password else False


def update_teacher_prompt(id, prompt, memo, model, creator, public):
    conn = connect_db()
    with conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE teacher set prompt = ?, memo = ?, model = ?, creator = ?, public = ? where ID = ?",
            (prompt, memo, model, creator, public, id),
        )
    return


def delete_prompt(table, id):
    conn = connect_db()
    with conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table} WHERE ID = ?", (id,))
    return


def insert_teacher_prompt(prompt, memo, model, creator, public):
    conn = connect_db()
    with conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO teacher (prompt, memo, model, creator, public) VALUES (?, ?, ?, ?, ?)",
            (prompt, memo, model, creator, public),
        )
    return


def select_teacher_prompt(creator):
    conn = connect_db()
    with conn:
        prompts = pd.read_sql(
            "SELECT * FROM teacher WHERE creator = ? OR public = True",
            con=conn,
            params=[creator],
        )
    return prompts.to_dict(orient="records")


def select_model():
    conn = connect_db()
    with conn:
        models = pd.read_sql("SELECT name, module FROM models WHERE use=True", con=conn)
    return models.to_dict(orient="records")


def select_all_model():
    models = pd.read_sql("SELECT * FROM model", con=engine, index_col='id')
    return models


def update_all_model(models: pd.DataFrame):
    dtype = {
        "id": Integer,
        "use": Integer,
        "free": Integer,
        "platform": Text,
        "series": Text,
        "name": Text,
        "module": Text,
        "price_input": Float,
        "price_output": Float,
    }
    models.to_sql(name="model", con=engine, if_exists="replace", index=True, index_label='id', dtype=dtype)
    with Session() as session:
        session.execute(text("ALTER TABLE `model` COLUMN `id` INTERGER PRIMARY KEY AUTOINCREMENT"))
        session.commit()
    return
