# from libs.bvcdatabase import Case, create_table, Chapter
# create_table(Chapter)

from libs.bvcdatabase import Teacher, Case, Chapter, Session
from sqlalchemy import select, delete

with Session() as session:
    # teacher = session.execute(select(Teacher).where(Teacher.id == 1)).scalar()
    # chapter = session.execute(select(Chapter).where(Chapter.id == 1)).scalar()
    # case = Case(
    #     teacher=teacher,
    #     chapter=chapter,
    #     profile="test_profile",
    #     content="test_content",
    #     creator="dearfad",
    # )
    # session.add(case)
    # session.commit()
    # result = session.execute(select(Chapter).where(Chapter.id == 1)).scalar()
    # print(result.chapter_cases[0].content)

    # session.execute(delete(Chapter).where(Chapter.id == 4))
    # session.commit()
    # result = session.execute(select(Case).where(Case.id==1)).scalar()
    # print(result.chapter.name)
    chapter = Chapter(book='1', name='2', subject="3")
    session.add(chapter)
    session.commit()