from ntpath import join
from sqlalchemy.orm import Session

from schemas import AnswerCreate
from models import Alternative, AlternativeAnswer, Research


def create_answer(
    db: Session, answer: AnswerCreate, research_id: int, alternative_id: int
):
    db_awnser = AlternativeAnswer(
        **answer.dict(), research_id=research_id, alternative_id=alternative_id
    )
    db.add(db_awnser)
    db.commit()


def get_answers_of_research(db: Session, research_id: int, owner_id: int):
    return (
        db.query(AlternativeAnswer)
        .join(Research)
        .join(Alternative)
        .filter(Research.owner_id == owner_id, Research.id == research_id)
        .all()
    )
