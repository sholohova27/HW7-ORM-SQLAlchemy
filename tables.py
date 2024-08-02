from sqlalchemy import Integer, String, ForeignKey, DateTime, create_engine
from sqlalchemy.orm import relationship, Mapped, mapped_column, sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
import psycopg2

Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    # Обратная связь
    students = relationship("Student", back_populates="group")


class Student(Base):
    __tablename__ = 'students'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    group_id_fn: Mapped[int] = mapped_column(Integer, ForeignKey('groups.id'))

    group = relationship("Group", back_populates="students")
    marks = relationship("Marks", back_populates="student")


class Lector(Base):
    __tablename__ = 'lectors'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    # Обратная связь
    subjects = relationship("Subject", back_populates="lector")


class Subject(Base):
    __tablename__ = 'subjects'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    lector_id_fn: Mapped[int] = mapped_column(Integer, ForeignKey('lectors.id'))

    lector = relationship("Lector", back_populates="subjects")
    marks = relationship("Marks", back_populates="subject")


class Marks(Base):
    __tablename__ = 'marks'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    subject_id_fn: Mapped[int] = mapped_column(Integer, ForeignKey('subjects.id', ondelete='SET NULL'), nullable=True)
    student_id_fn: Mapped[int] = mapped_column(Integer, ForeignKey('students.id', ondelete='CASCADE'))
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=func.now())

    student = relationship("Student", back_populates="marks")
    subject = relationship("Subject", back_populates="marks")


DATABASE_URL = "postgresql+psycopg2://nataly:123456@localhost:5433/my-postgres"


engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

