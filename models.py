from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref

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


class Research(_db.Base):
    __tablename__ = "researches"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="researches")
    questionnaires = relationship(
        "Questionnaire", back_populates="research", cascade="all, delete-orphan"
    )


class Questionnaire(_db.Base):
    __tablename__ = "questionnaires"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    public = Column(String)
    research_id = Column(Integer, ForeignKey("researches.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="questionnaires")
    research = relationship(
        "Research", back_populates="questionnaires", cascade="all, delete-orphan"
    )
    questions = relationship(
        "Question", back_populates="questionnaire", cascade="all, delete-orphan"
    )


class Question(_db.Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String)
    order = Column(Integer)
    questionnaire_id = Column(Integer, ForeignKey("questionnaires.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="questions")
    questionnaire = relationship(
        "Questionnaire", back_populates="questions", cascade="all, delete-orphan"
    )
    alternatives = relationship(
        "Alternative", back_populates="question", cascade="all, delete-orphan"
    )


class Alternative(_db.Base):
    __tablename__ = "alternatives"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    text = Column(String)
    value = Column(Integer)
    question_id = Column(Integer, ForeignKey("questions.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship(
        "User", back_populates="alternatives", cascade="all, delete-orphan"
    )
    question = relationship("Question", back_populates="alternatives")
