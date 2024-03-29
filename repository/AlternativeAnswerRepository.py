from sqlalchemy.orm import Session

from schemas import AnswerCreate, AwnserBulkCreate
from models import (
    Alternative,
    AlternativeAnswer,
    Question,
    Questionnaire,
    Research,
)


def create_answer(
    db: Session, answer: AnswerCreate, research_id: int, alternative_id: int
):
    db_awnser = AlternativeAnswer(
        **answer.dict(), research_id=research_id, alternative_id=alternative_id
    )
    db.add(db_awnser)
    db.commit()


def get_answers_of_research(db: Session, research_id: int, owner_id: int):
    query = (
        db.query(AlternativeAnswer)
        .join(AlternativeAnswer.alternative)
        .join(Alternative.question)
        .join(Question.questionnaire)
        .join(Questionnaire.research)
        .join(AlternativeAnswer.subject)
        .filter(
            Research.owner_id == owner_id,
            Research.id == research_id,
            Alternative.text != "placeholder",
        )
    )
    print(query)
    return query.all()


def create_bulk_answers(
    db: Session, answers: AwnserBulkCreate, research_id: int, subject_id: int
):
    alternativeAnswers = [
        AlternativeAnswer(
            **answer.dict(), research_id=research_id, subject_id=subject_id
        )
        for answer in answers.alternatives
    ]
    db.bulk_save_objects(alternativeAnswers)
    db.commit()
