import pandas as pd
import streamlit as st
from sqlalchemy import (
    Float,
    ForeignKey,
    Integer,
    Text,
    create_engine,
    delete,
    select,
    update,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)

engine = create_engine("sqlite:///data/clinic.db")
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(Text, nullable=False)


class Model(Base):
    __tablename__ = "model"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    use: Mapped[bool] = mapped_column(Integer, nullable=True)
    free: Mapped[bool] = mapped_column(Integer, nullable=True)
    platform: Mapped[str] = mapped_column(Text, nullable=True)
    series: Mapped[str] = mapped_column(Text, nullable=True)
    name: Mapped[str] = mapped_column(Text, nullable=True)
    module: Mapped[str] = mapped_column(Text, nullable=True)
    price_input: Mapped[float] = mapped_column(Float, nullable=True)
    price_output: Mapped[float] = mapped_column(Float, nullable=True)


class Teacher(Base):
    __tablename__ = "teacher"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    prompt: Mapped[str] = mapped_column(Text, nullable=True)
    memo: Mapped[str] = mapped_column(Text, nullable=True)
    model: Mapped[str] = mapped_column(Text, nullable=True)
    creator: Mapped[str] = mapped_column(Text, nullable=True)
    public: Mapped[bool] = mapped_column(Integer, nullable=True)

    teacher_cases: Mapped[list['Case']] = relationship(back_populates='teacher')


class Chapter(Base):
    __tablename__ = "chapter"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement="auto")
    book: Mapped[str] = mapped_column(Text, nullable=True)
    name: Mapped[str] = mapped_column(Text, nullable=True)
    subject: Mapped[str] = mapped_column(Text, nullable=True)

    chapter_cases: Mapped[list['Case']] = relationship(back_populates='chapter')

class Case(Base):
    __tablename__ = "case"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher.id", ondelete="SET NULL"), nullable=True)
    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapter.id", ondelete="SET NULL"), nullable=True)
    profile: Mapped[str] = mapped_column(Text, nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    creator: Mapped[str] = mapped_column(Text, nullable=True)

    teacher: Mapped[Teacher] = relationship(lazy=False, back_populates="teacher_cases")
    chapter: Mapped[Chapter] = relationship(lazy=False, back_populates='chapter_cases')


def create_table(table: Base):
    Base.metadata.create_all(engine, tables=[table.__table__])


def user_register(username, password):
    with Session() as session:
        user = User(name=username, password=password, role="student")
        session.add(user)
        session.commit()


def check_user_exist(username: str) -> bool:
    with Session() as session:
        result = session.execute(select(User).where(User.name == username))
        user = result.scalar()
    return True if user else False


def user_login(username, password):
    with Session() as session:
        result = session.execute(select(User).where(User.name == username))
        user = result.scalar_one()
    return True if user and user.password == password else False


def get_user_role(username):
    with Session() as session:
        result = session.execute(select(User).where(User.name == username))
        user = result.scalar()
    return user.role


def change_user_role(username, role):
    with Session() as session:
        session.execute(update(User).where(User.name == username).values(role=role))
        session.commit()
    return


def update_teacher_prompt(id, prompt, memo, model, creator, public):
    with Session() as session:
        session.execute(
            update(Teacher)
            .where(Teacher.id == id)
            .values(
                prompt=prompt, memo=memo, model=model, creator=creator, public=public
            )
        )
        session.commit()
    return


def delete_teacher_prompt(id):
    with Session() as session:
        session.execute(delete(Teacher).where(Teacher.id == id))
        session.commit()
    return


def add_teacher_prompt(prompt, memo, model, creator, public):
    with Session() as session:
        teacher_prompt = Teacher(
            prompt=prompt, memo=memo, model=model, creator=creator, public=public
        )
        session.add(teacher_prompt)
        session.commit()
    return


def select_teacher_prompt(creator):
    return pd.read_sql(
        "SELECT * FROM teacher WHERE creator = ? OR public = True",
        con=engine,
        params=(creator,),
    ).to_dict(orient="records")


def select_model():
    return pd.read_sql(
        "SELECT name, module FROM model WHERE use=True", con=engine
    ).to_dict(orient="records")


def select_all_model():
    return pd.read_sql("SELECT * FROM model", con=engine)


def update_all_model(models: pd.DataFrame):
    with Session() as session:
        session.bulk_update_mappings(Model, models.to_dict(orient="records"))
        session.commit()
    return


@st.dialog("添加模型")
def add_model():
    use = st.checkbox("使用")
    free = st.checkbox("免费")
    platform = st.text_input("平台")
    series = st.text_input("系列")
    name = st.text_input("名称")
    module = st.text_input("模块")
    price_input = st.number_input("输入价格")
    price_output = st.number_input("输出价格")
    col_confirm, col_cancel = st.columns(2)
    with col_confirm:
        if st.button("**添加**", use_container_width=True):
            model = Model(
                use=use,
                free=free,
                platform=platform,
                series=series,
                name=name,
                module=module,
                price_input=price_input,
                price_output=price_output,
            )
            with Session() as session:
                session.add(model)
                session.commit()
            st.rerun()
    with col_cancel:
        if st.button("**取消**", use_container_width=True):
            st.rerun()


@st.dialog("删除模型")
def delete_model(models: pd.DataFrame):
    id = st.number_input("id", min_value=1, step=1)
    model = models.loc[models["id"] == id]
    if not model.empty:
        model.columns = [
            "ID",
            "使用",
            "免费",
            "平台",
            "系列",
            "名称",
            "模块",
            "输入价格",
            "输出价格",
        ]
        model = model.astype(str)
        model_T = model.T.reset_index()
        model_T.columns = ["name", "info"]
        st.dataframe(
            model_T,
            use_container_width=True,
            hide_index=True,
            column_config={
                "name": st.column_config.TextColumn(
                    "项目",
                ),
                "info": st.column_config.TextColumn(
                    "信息",
                ),
            },
        )
    else:
        st.markdown("没有相关模型")
    col_confirm, col_cancel = st.columns(2)
    with col_confirm:
        if st.button("**删除**", use_container_width=True):
            with Session() as session:
                session.execute(delete(Model).where(Model.id == id))
                session.commit()
            st.rerun()
    with col_cancel:
        if st.button("**取消**", use_container_width=True):
            st.rerun()


@st.dialog("更改权限")
def change_role():
    username = st.text_input("**用户名**")
    role = st.selectbox("**权限**", ["student", "teacher"])
    if st.button("更改"):
        change_user_role(username, role)
        st.rerun()


@st.dialog("添加章节")
def add_chapter():
    book = st.text_input("**教科书**")
    name = st.text_input("**章节**")
    subject = st.text_input("**主题**")
    if st.button("添加"):
        with Session() as session:
            chapter = Chapter(book=book, name=name, subject=subject)
            session.add(chapter)
            session.commit()
        st.rerun()
