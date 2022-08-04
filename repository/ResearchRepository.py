from sqlalchemy.orm import Session

from schemas import ResearchCreate
from models import Research


def get_all_researches_by_user(db: Session, owner_id: str):
    return db.query(Research).filter(Research.owner_id == owner_id).all()


def get_one_research_by_id(db: Session, owner_id: str, research_id: str):
    return (
        db.query(Research)
        .filter(Research.owner_id == owner_id, Research.id == research_id)
        .first()
    )


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


def save_existing_research(db: Session, research: Research) -> Research:
    db.add(research)
    db.commit()
    db.refresh(research)
    return research
