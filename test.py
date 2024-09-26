from libs.bvcdatabase import Cases, create_table, Chapter
create_table(Cases)

# from libs.bvcdatabase import Teacher, Case, Chapter, Session
# from sqlalchemy import select, delete

# with Session() as session:
    # teacher = session.execute(select(Teacher).where(Teacher.id == 3)).scalar()
    # chapter = session.execute(select(Chapter).where(Chapter.id == 8)).scalar()
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

    # session.execute(delete(Chapter).where(Chapter.id == 8))
    # session.commit()

    # result = session.execute(select(Case).where(Case.id==1)).scalar()
    # print(result.chapter.name)

    # chapter = Chapter(book='1', name='2', subject="3")
    # session.add(chapter)
    # session.commit()

    # chapter = session.execute(select(Chapter).where(Chapter.id==8)).scalar()
    # session.delete(chapter)
    # session.commit()

# import streamlit as st

# st.text_input('input', key='test1')

# def up():
#     st.session_state.test2 = 'ok'


# if st.button('run', on_click=up):
#     # st.rerun()
#     pass