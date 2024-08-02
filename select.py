from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from tables import Student, Group, Lector, Subject, Marks, SessionLocal



def select_1(session: Session):
    # ТОП-5 студентов по среднему баллу
    results = session.query(Student, func.avg(Marks.value).label('avg_grade')).\
        join(Marks, isouter=True).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
    
    formatted_results = []
    for student, avg_grade in results:
        formatted_results.append({
            'Student ID': student.id,
            'Student Name': student.name,
            'Average Grade': round(float(avg_grade), 1)
        })
    return formatted_results



def select_2(session: Session, subject_id: int):
    # Лучший студент по предмету
    result = session.query(Student, func.avg(Marks.value).label('avg_grade')).\
        join(Marks, isouter=True).filter(Marks.subject_id_fn == subject_id).\
        group_by(Student.id).order_by(desc('avg_grade')).first()

    if result:
        student, avg_grade = result
        return [{
            'Student ID': student.id,
            'Student Name': student.name,
            'Average Grade': round(float(avg_grade), 1)
        }]
    else:
        return None

# isouter=True = left join

def select_3(session: Session, subject_id: int):
    # Средний балл по группам по предмету
    results = session.query(Group, func.avg(Marks.value).label('avg_grade')).\
        select_from(Student).join(Group).join(Marks).filter(Marks.subject_id_fn == subject_id).\
        group_by(Group.id).all()
    formatted_results = []

    for group, avg_grade in results:
        formatted_results.append({
            'Group id': group.id,
            'Group name': group.name,
            'Average Grade': round(float(avg_grade), 1)
        })
    return formatted_results


def select_4(session: Session):
    # Средний балл на потоке
    avg_grade = session.query(func.avg(Marks.value)).scalar()
    if avg_grade is not None:
        return round(float(avg_grade), 1)
    return None


def select_5(session: Session, lector_id: int):
    # Курсы лектора
    results = session.query(Subject).filter(Subject.lector_id_fn == lector_id).all()

    formatted_results = []

    for subject in results:
        formatted_results.append({
            'Subject id': subject.id,
            'Subject name': subject.name
        })
    return formatted_results


def select_6(session: Session, group_id: int):
    # Студенты по группам
    results = session.query(Student).filter(Student.group_id_fn == group_id).all()

    formatted_results = []
    for student in results:
        formatted_results.append({
            'Student ID': student.id,
            'Student Name': student.name
        })
    return formatted_results


def select_7(session: Session, group_id: int, subject_id: int):
    # НСтуденты по группам и предметам
    results = session.query(Student.name, Marks.value).\
        join(Marks).\
        filter(Student.group_id_fn == group_id, Marks.subject_id_fn == subject_id).all()

    formatted_results = []
    for student_name, grade in results:
        formatted_results.append({
            'Student Name': student_name,
            'Grade': grade
        })
    return formatted_results


def select_8(session: Session, lector_id: int):
    # Средний балл преподавателя по предмету
    avg_grade = session.query(func.avg(Marks.value)).\
        join(Subject).filter(Subject.lector_id_fn == lector_id).scalar()

    if avg_grade is not None:
        return round(float(avg_grade), 1)
    return None


def select_9(session: Session, student_id: int):
    # Список курсов по студенту
    results = session.query(Subject).\
        join(Marks).filter(Marks.student_id_fn == student_id).group_by(Subject.id).all()

    formatted_results = []
    for subject in results:
        formatted_results.append({
            'Subject ID': subject.id,
            'Subject Name': subject.name
        })
    return formatted_results


def select_10(session: Session, student_id: int, lector_id: int):
    # Список курсов по студенту и преподавателю
    results = session.query(Subject).\
        join(Marks).\
        filter(Marks.student_id_fn == student_id, Subject.lector_id_fn == lector_id).\
        group_by(Subject.id).all()

    formatted_results = []
    for subject in results:
        formatted_results.append({
            'Subject ID': subject.id,
            'Subject Name': subject.name
        })
    return formatted_results



if __name__ == "__main__":
    # with SessionLocal() as session:
    #     result = select_4(session)
    #     print(result)

    try:
        with SessionLocal() as session:
            results = select_10(session, 1, 2)

            if results:
                for result in results:
                    print(result)
            else:
                print("There are no results by this condition")
    except Exception as e:
        print(f"An error occurred while accessing the database: {e}")

