import sqlite3

import pandas as pd


def check_user_exist(username):
    conn = sqlite3.connect("data/clinic.db")
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM users WHERE name = ?", (username,))
        user = cursor.fetchone()
    return True if user else False


def user_register(username, password):
    conn = sqlite3.connect("data/clinic.db")
    with conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, password) VALUES (?, ?)", (username, password)
        )
    return


def user_login(username, password):
    conn = sqlite3.connect("data/clinic.db")
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE name = ?", (username,))
        user = cursor.fetchone()
    return True if user and user[0] == password else False


def update_teacher_prompt(id, prompt, memo, model, creator, public):
    conn = sqlite3.connect("data/clinic.db")
    with conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE teacher set prompt = ?, memo = ?, model = ?, creator = ?, public = ? where ID = ?", (prompt, memo, model, creator, public, id)
        )
    return


def delete_prompt(table, id):
    conn = sqlite3.connect("data/clinic.db")
    with conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table} WHERE ID = ?", (id,))
    return


def insert_teacher_prompt(prompt, memo, model, creator, public):
    conn = sqlite3.connect("data/clinic.db")
    with conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO teacher (prompt, memo, model, creator, public) VALUES (?, ?, ?, ?, ?)", (prompt, memo, model, creator, public)
        )
    return


def select_teacher_prompt(creator):
    conn = sqlite3.connect("data/clinic.db")
    with conn:
        prompts = pd.read_sql("SELECT * FROM teacher WHERE creator = ? OR public = True", con=conn, params=[creator])
    return prompts.to_dict(orient="records")

def select_model():
    connect = sqlite3.connect("data/clinic.db")
    with connect:
        models = pd.read_sql(
            "SELECT name, module FROM models WHERE use=True", con=connect
        )
    return models.to_dict(orient="records")