from sqlalchemy.orm import Session
from passlib.context import CryptContext

from models import Alternative
from schemas import AlternativeCreate


def get_all_alternatives_by_question(db: Session, question_id: int, owner_id: int):
    return (
        db.query(Alternative)
        .filter(
            Alternative.question_id == question_id, Alternative.owner_id == owner_id
        )
        .all()
    )


def create_alternative(
    db: Session, alternative: AlternativeCreate, question_id: int, owner_id: int
):
    db_alternative = Alternative(
        **alternative.dict(), question_id=question_id, owner_id=owner_id
    )
    db.add(db_alternative)
    db.commit()
    db.refresh(db_alternative)
    return db_alternative


def update_alternative(
    db: Session,
    alternative: AlternativeCreate,
    question_id: int,
    id: int,
    owner_id: int,
):
    db.query(Alternative).filter(
        Alternative.question_id == question_id,
        Alternative.id == id,
        Alternative.owner_id == owner_id,
    ).update(
        values={
            Alternative.text: alternative.text,
            Alternative.type: alternative.type,
            Alternative.value: alternative.value,
        }
    )
    db.commit()


def delete_alternative(db: Session, question_id: int, id: int, owner_id):
    db.query(Alternative).filter(
        Alternative.question_id == question_id,
        Alternative.id == id,
        Alternative.owner_id == owner_id,
    ).delete()
    db.commit()


def add_alternative_from_template(
    db: Session, original_question_id: int, owner_id: int, new_question_id: int
):
    original_alternatives = (
        db.query(Alternative)
        .filter(Alternative.question_id == original_question_id)
        .all()
    )
    for original_alternative in original_alternatives:
        new_alternative = Alternative(
            type=original_alternative.type,
            text=original_alternative.text,
            value=original_alternative.value,
            question_id=new_question_id,
            owner_id=owner_id,
        )
        db.add(new_alternative)
    db.commit()
