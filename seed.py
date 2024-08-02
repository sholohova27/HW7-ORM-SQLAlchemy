from sqlalchemy.orm import Session
from faker import Faker
from tables import Student, Group, Lector, Subject, Marks, engine, SessionLocal, Base
import random
import psycopg2

fake = Faker()


def generate_fake_groups(session: Session, number, start_id):
    group_id = []
    used_words = set()
    group_list = ['Marketing', 'IT', 'PR', 'Art', 'Literature', 'History']
    for i in range(start_id, start_id + number):
        while True:
            group_name = random.choice(group_list)
            if group_name not in used_words:
                break
        used_words.add(group_name)
        group = Group(id=i,
                      name=group_name)
        session.add(group)
        session.commit()
        group_id.append(i)
    return group_id


def generate_fake_students(session: Session, number, start_id, group_id):
    student_id = []
    for i in range(start_id, start_id + number):
        student = Student(id=i,
                          name=fake.name(),
                          group_id_fn=fake.random_element(group_id))
        session.add(student)
        session.commit()
        student_id.append(i)
        return student_id


def generate_fake_marks(session: Session, number, start_id, subject_id, student_id):
    for i in range(start_id, start_id + number):
        mark = Marks(id=i,
                     value=fake.random_int(min=1, max=100),
                     subject_id_fn=fake.random_element(subject_id),
                     student_id_fn=fake.random_element(student_id))
        session.add(mark)
        session.commit()


def generate_fake_lectors(session: Session, number, start_id):
    lector_id = []
    for i in range(start_id, start_id + number):
        lector = Lector(id=i,
                        name=fake.name())
        session.add(lector)
        session.commit()
        lector_id.append(i)
        return lector_id

def generate_fake_subjects(session: Session, number, start_id, lector_id):
    subject_id = []
    subject_list = ['Math', 'Literature', 'History', 'Databases', 'Data Science']
    used_subjects = set()
    for i in range(start_id, start_id + number):
        while True:
            subject_name = random.choice(subject_list)
            if subject_name not in used_subjects:
                break
        used_subjects.add(subject_name)
        subject = Subject(id=i, name=subject_name, lector_id_fn=fake.random_element(lector_id))
        session.add(subject)
        session.commit()
        subject_id.append(i)
        return subject_id

def main():
    with SessionLocal() as session:
        group_id = generate_fake_groups(session,3, 1)
        student_id = generate_fake_students(session,  30,1, group_id)
        lector_id = generate_fake_lectors(session, 5, 1)
        subject_id = generate_fake_subjects(session, 5, 1, lector_id)
        generate_fake_marks(session, 1500, 1, subject_id, student_id)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    main()
