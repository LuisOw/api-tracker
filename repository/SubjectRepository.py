from sqlalchemy.orm import Session
from passlib.context import CryptContext

import models
import schemas


def get_subject(db: Session, subject_id: int):
    return db.query(models.Subject).filter(models.Subject.id == subject_id).first()


def get_subject_by_username(db: Session, username: str):
    return db.query(models.Subject).filter(models.Subject.username == username).first()


def create_subject(
    db: Session, subject: schemas.SubjectCreate, pwd_context: CryptContext
):
    hashed_password = pwd_context.hash(subject.password)
    db_subject = models.Subject(
        username=subject.username,
        hashed_password=hashed_password,
        chosen_name=subject.chosen_name,
    )
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject
