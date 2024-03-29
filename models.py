from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table, Date
from sqlalchemy.orm import relationship

import database as _db


class User(_db.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)

    researches = relationship("Research", back_populates="owner")
    questionnaires = relationship("Questionnaire", back_populates="owner")
    questions = relationship("Question", back_populates="owner")
    alternatives = relationship("Alternative", back_populates="owner")


research_subject = Table(
    "research_subject",
    _db.Base.metadata,
    Column("subject_id", ForeignKey("subjects.id"), primary_key=True),
    Column("research_id", ForeignKey("researches.id"), primary_key=True),
)


class Subject(_db.Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    chosen_name = Column(String)
    hashed_password = Column(String)
    birth_date = Column(Date)
    income = Column(Integer)
    race = Column(String)
    gender = Column(String)
    sexualOrientation = Column(String)

    researches = relationship(
        "Research", secondary=research_subject, back_populates="subjects"
    )
    alternatives_answer = relationship("AlternativeAnswer", back_populates="subject")
    usage_time = relationship("UsageTime", back_populates="subject")


class Research(_db.Base):
    __tablename__ = "researches"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    visibility = Column(String)
    state = Column(String)
    startTime = Column(DateTime)
    endTime = Column(DateTime)
    initialAge = Column(Integer)
    finalAge = Column(Integer)
    initialIncome = Column(Integer)
    finalIncome = Column(Integer)
    race = Column(String)
    gender = Column(String)
    sexualOrientation = Column(String)
    code = Column(String)
    modules = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="researches")
    questionnaires = relationship(
        "Questionnaire", back_populates="research", cascade="all, delete-orphan"
    )
    alternative_answers = relationship(
        "AlternativeAnswer", back_populates="research", cascade="all, delete-orphan"
    )
    subjects = relationship(
        "Subject", secondary=research_subject, back_populates="researches"
    )


class Questionnaire(_db.Base):
    __tablename__ = "questionnaires"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    public = Column(String)
    research_id = Column(Integer, ForeignKey("researches.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="questionnaires")
    research = relationship("Research", back_populates="questionnaires")
    questions = relationship(
        "Question", back_populates="questionnaire", cascade="all, delete-orphan"
    )


class Question(_db.Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String)
    order = Column(Integer)
    type = Column(String)
    questionnaire_id = Column(Integer, ForeignKey("questionnaires.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="questions")
    questionnaire = relationship("Questionnaire", back_populates="questions")
    alternatives = relationship(
        "Alternative", back_populates="question", cascade="all, delete-orphan"
    )


class Alternative(_db.Base):
    __tablename__ = "alternatives"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    value = Column(Integer)
    question_id = Column(Integer, ForeignKey("questions.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="alternatives")
    question = relationship("Question", back_populates="alternatives")
    alternative_answers = relationship(
        "AlternativeAnswer", back_populates="alternative", cascade="all, delete-orphan"
    )


class AlternativeAnswer(_db.Base):
    __tablename__ = "alternatives_answer"

    id = Column(Integer, primary_key=True, index=True)
    alternative_chosen = Column(String)
    text = Column(String)
    alternative_id = Column(Integer, ForeignKey("alternatives.id"))
    research_id = Column(Integer, ForeignKey("researches.id"), index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), index=True)

    alternative = relationship("Alternative", back_populates="alternative_answers")
    research = relationship("Research", back_populates="alternative_answers")
    subject = relationship("Subject", back_populates="alternatives_answer")


class UsageTime(_db.Base):
    __tablename__ = "usage_time"

    id = Column(Integer, primary_key=True, index=True)
    collected_time = Column(String)
    subject_id = Column(Integer, ForeignKey("subjects.id"), index=True)

    subject = relationship("Subject", back_populates="usage_time")
