from sqlalchemy.orm import Session

from schemas import UsageTimeCreate
from models import UsageTime


def create_usage_time(db: Session, subject_id: int, usage_time: UsageTimeCreate):
    db_awnser = UsageTime(**usage_time.dict(), subject_id=subject_id)
    db.add(db_awnser)
    db.commit()


def delete_usage_time(db: Session, subject_id: int):
    db.query(UsageTime).filter(UsageTime.subject.has(id=subject_id)).delete(
        synchronize_session=False
    )
    db.commit()


def get_usage_time(db: Session):
    return db.query(UsageTime).join(UsageTime.subject).all()
