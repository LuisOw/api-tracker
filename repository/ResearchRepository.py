from sqlalchemy.orm import Session
from passlib.context import CryptContext

from schemas import ResearchCreate
from models import Research


def get_all_researches_by_user(db: Session, owner_id: str):
    return db.query(Research).filter(Research.owner_id == owner_id).all()


def create_research(db: Session, research: ResearchCreate, user_id: str, code: str):
    db_research = Research(
        **research.dict(), owner_id=user_id, state="inactive", code=code
    )
    db.add(db_research)
    db.commit()
    db.refresh(db_research)
    return db_research


def update_research(db: Session, research: ResearchCreate, owner_id: str, id: str):
    research_from_db = (
        db.query(Research)
        .filter(Research.owner_id == owner_id, Research.id == id)
        .first()
    )
    research_data = research.dict(exclude_unset=True)
    for key, value in research_data.items():
        setattr(research_from_db, key, value)
    db.add(research_from_db)
    db.commit()


def delete_research(db: Session, owner_id: str, research_id: str):
    research = (
        db.query(Research)
        .filter(Research.owner_id == owner_id, Research.id == research_id)
        .first()
    )
    db.delete(research)
    db.commit()
