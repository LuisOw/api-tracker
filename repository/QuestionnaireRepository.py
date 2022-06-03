from sqlalchemy.orm import Session
from passlib.context import CryptContext

from schemas import QuestionnaireCreate
from models import Questionnaire


def get_all_questionnaires_by_research(db: Session, research_id: int, owner_id: int):
    return (
        db.query(Questionnaire)
        .filter(
            Questionnaire.research_id == research_id, Questionnaire.owner_id == owner_id
        )
        .all()
    )


def create_questionnaire(
    db: Session, questionnaire: QuestionnaireCreate, research_id: int, owner_id: int
):
    db_questionnaire = Questionnaire(
        **questionnaire.dict(), research_id=research_id, owner_id=owner_id
    )
    db.add(db_questionnaire)
    db.commit()
    db.refresh(db_questionnaire)
    return db_questionnaire


def update_questionnaire(
    db: Session,
    questionnaire: QuestionnaireCreate,
    research_id: int,
    id: int,
    owner_id: int,
):
    db.query(Questionnaire).filter(
        Questionnaire.research_id == research_id,
        Questionnaire.id == id,
        Questionnaire.owner_id == owner_id,
    ).update(
        values={
            Questionnaire.title: questionnaire.title,
            Questionnaire.public: questionnaire.public,
        }
    )
    db.commit()


def delete_questionnaire(db: Session, research_id: int, id: int, owner_id: int):
    db.query(Questionnaire).filter(
        Questionnaire.research_id == research_id,
        Questionnaire.id == id,
        Questionnaire.owner_id == owner_id,
    ).delete()
    db.commit()
