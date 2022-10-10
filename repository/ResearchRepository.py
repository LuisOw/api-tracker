from sqlalchemy.orm import Session

from schemas import ResearchCreate
from models import Research, Subject


def get_all_researches_by_user(db: Session, owner_id: str):
    return db.query(Research).filter(Research.owner_id == owner_id).all()


def get_all_researches_by_subject(db: Session, id: str):
    return db.query(Research).filter(Research.subjects.any(id=id)).all()


def get_one_research_by_id(db: Session, owner_id: str, research_id: str):
    return (
        db.query(Research)
        .filter(Research.owner_id == owner_id, Research.id == research_id)
        .first()
    )


def get_one_research_by_id_without_owner(db: Session, research_id: str):
    return db.query(Research).filter(Research.id == research_id).first()


def create_research(
    db: Session, research: ResearchCreate, user_id: str, code: str
) -> Research:
    db_research = Research(
        **research.dict(), owner_id=user_id, state="inativa", code=code
    )
    db.add(db_research)
    db.commit()
    db.refresh(db_research)
    return db_research


def update_research(db: Session, research: ResearchCreate, research_from_db: Research):
    research_data = research.dict(exclude_unset=True)
    for key, value in research_data.items():
        setattr(research_from_db, key, value)
    db.add(research_from_db)
    db.commit()


def delete_research(db: Session, owner_id: str, research_id: str):
    research_from_db = get_one_research_by_id(
        db=db, owner_id=owner_id, research_id=research_id
    )
    db.delete(research_from_db)
    db.commit()


def delete_research_admin(db: Session, research_id: str):
    research_from_db = get_one_research_by_id(db=db, research_id=research_id)
    db.delete(research_from_db)
    db.commit()


def save_existing_research(db: Session, research: Research) -> Research:
    db.add(research)
    db.commit()
    db.refresh(research)
    return research


def add_subject(db: Session, subject: Subject, id: int):
    research = get_one_research_by_id_without_owner(db, id)
    research.subjects.append(subject)
    db.add(research)
    db.commit()


def get_all_filtered(db: Session, subject: Subject, age: int = None):
    filters = [Research.state != "encerrada"]
    filters.append(Research.visibility != "privado")

    if subject.gender:
        filters.append(Research.gender == subject.gender)
    if subject.race:
        filters.append(Research.race == subject.race)
    if subject.sexualOrientation:
        filters.append(Research.sexualOrientation == subject.sexualOrientation)
    if age:
        filters.append(Research.initialAge <= age)
        filters.append(Research.finalAge >= age)
    if subject.income:
        filters.append(Research.initialIncome <= subject.income)
        filters.append(Research.finalIncome >= subject.income)

    return db.query(Research).filter(*filters).all()


def check_subject(db: Session, subject_id: int, research_id: int):
    return (
        db.query(Research)
        .filter(Research.id == research_id, Research.subjects.any(id=subject_id))
        .first()
    )
