import sqlite3

import pandas as pd


def connect_db():
    return sqlite3.connect("data/clinic.db")


def check_user_exist(username):
    conn = connect_db()
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM users WHERE name = ?", (username,))
        user = cursor.fetchone()
    return True if user else False


def user_register(username, password):
    conn = connect_db()
    with conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, password) VALUES (?, ?)", (username, password)
        )
    return


def user_login(username, password):
    conn = connect_db()
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE name = ?", (username,))
        user = cursor.fetchone()
    return True if user and user[0] == password else False


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
    conn = connect_db()
    with conn:
        models = pd.read_sql("SELECT * FROM models", con=conn, index_col="id")
    return models


def update_all_model(models: pd.DataFrame):
    conn = connect_db()
    with conn:
        models.to_sql(name="models", con=conn, if_exists="replace", index=True)
    return
