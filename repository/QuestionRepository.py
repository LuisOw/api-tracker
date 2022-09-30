from sqlalchemy.orm import Session
from passlib.context import CryptContext

from models import Question
from models import Alternative
from schemas import QuestionCreate


def get_all_questions_by_questionnaire(
    db: Session, questionnaire_id: int, owner_id: int
):
    return (
        db.query(Question)
        .filter(
            Question.questionnaire_id == questionnaire_id, Question.owner_id == owner_id
        )
        .all()
    )


def get_all_questions_by_questionnaire_template(db: Session, questionnaire_id: int):
    return (
        db.query(Question).filter(Question.questionnaire_id == questionnaire_id).all()
    )


def create_question(
    db: Session, question: QuestionCreate, questionnaire_id: str, owner_id: int
):
    db_question = Question(
        **question.dict(), questionnaire_id=questionnaire_id, owner_id=owner_id
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def update_question(
    db: Session, question: QuestionCreate, questionnaire_id: int, id: int, owner_id: int
):
    db.query(Question).filter(
        Question.questionnaire_id == questionnaire_id,
        Question.id == id,
        Question.owner_id == owner_id,
    ).update(
        values={
            Question.query: question.query,
            Question.order: question.order,
            Question.type: question.type,
        }
    )
    db.commit()


def delete_question(db: Session, questionnaire_id: int, id: int, owner_id: int):
    question = (
        db.query(Question)
        .filter(
            Question.questionnaire_id == questionnaire_id,
            Question.id == id,
            Question.owner_id == owner_id,
        )
        .first()
    )
    db.delete(question)
    db.commit()


def add_questions_from_template(
    db: Session, owner_id: int, new_questionnaire_id: int, original_question: Question
):

    db_question = Question(
        query=original_question.query,
        order=original_question.order,
        questionnaire_id=new_questionnaire_id,
        owner_id=owner_id,
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def get_complete_questions_by_questionnaire_for_subject(
    db: Session, questionnaire_id: int
):
    return (
        db.query(Question)
        .join(Alternative)
        .filter(Question.questionnaire_id == questionnaire_id)
        .all()
    )


def get_by_id(db: Session, question_id: int, owner_id: int):
    return (
        db.query(Question)
        .filter(Question.id == question_id, Question.owner_id == owner_id)
        .first()
    )
