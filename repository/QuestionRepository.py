from sqlalchemy.orm import Session
from passlib.context import CryptContext

from models import Question
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
        }
    )
    db.commit()


def delete_question(db: Session, questionnaire_id: int, id: int, owner_id: int):
    db.query(Question).filter(
        Question.questionnaire_id == questionnaire_id,
        Question.id == id,
        Question.owner_id == owner_id,
    ).delete()
    db.commit()
