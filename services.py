import random, string
from typing import List
import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm
import email_validator as _email_check
from passlib.context import CryptContext


import database as _db
import repository.UserRepository as _userRepo
import repository.ResearchRepository as _researchRepo
import repository.QuestionnaireRepository as _questionnaireRepo
import repository.QuestionRepository as _questionRepo
import repository.AlternativeRepository as _alternativeRepo
import auth.AuthHandle as _auth
import schemas as _schemas


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2schema = _security.OAuth2PasswordBearer("/token")

_db.Base.metadata.create_all(bind=_db.engine)


def get_db():
    db = _db.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user(db: _orm.Session, user_id: int):
    return _userRepo.get_user(db, user_id)


def get_user_by_username(db: _orm.Session, username: str):
    return _userRepo.get_user_by_username(db, username)


def create_user(db: _orm.Session, user: _schemas.UserCreate):
    try:
        print(user.username)
        valid = _email_check.validate_email(email=user.username)
        username = valid.email
        user.username = username
    except _email_check.EmailNotValidError as e:
        raise Exception("Invalid email") from e

    return _userRepo.create_user(db, user, pwd_context=pwd_context)


def get_all_researches_by_user(db: _orm.Session, owner_id: int):
    return _researchRepo.get_all_researches_by_user(db, owner_id)


def create_research(db: _orm.Session, research: _schemas.ResearchCreate, user_id: int):
    code = ""
    if research.visibility == "privado":
        code = "".join(random.choices(string.ascii_letters + string.digits, k=10))
    return _researchRepo.create_research(db, research, user_id, code)


def update_research(
    db: _orm.Session, research: _schemas.ResearchCreate, owner_id: int, id: int
):
    _researchRepo.update_research(db=db, research=research, owner_id=owner_id, id=id)


def delete_research(db: _orm.Session, owner_id: int, research_id: int):
    _researchRepo.delete_research(db, owner_id, research_id)


def change_research_status(db: _orm.Session, owner_id: int, research_id: int):
    research = _researchRepo.get_one_research_by_id(
        db=db, owner_id=owner_id, research_id=research_id
    )
    print(research.status)
    return research


def get_all_questionnaires_by_research(
    db: _orm.Session, research_id: int, owner_id: int
):
    return _questionnaireRepo.get_all_questionnaires_by_research(
        db, research_id, owner_id
    )


def create_questionnaire(
    db: _orm.Session,
    questionnaire: _schemas.QuestionnaireCreate,
    research_id: int,
    owner_id: int,
):
    return _questionnaireRepo.create_questionnaire(
        db, questionnaire, research_id, owner_id
    )


def update_questionnaire(
    db: _orm.Session,
    questionnaire: _schemas.QuestionnaireCreate,
    research_id: int,
    id: int,
    owner_id: int,
):

    questionnaire_from_db = _questionnaireRepo.get_questionnaire(
        db=db, research_id=research_id, id=id, owner_id=owner_id
    )
    if (
        questionnaire_from_db.public == "template"
        and questionnaire.public != "template"
    ):
        raise ValueError(
            "Questionnaires of type template should not be changed to private or public"
        )
    _questionnaireRepo.update_questionnaire(
        db, questionnaire, research_id, id, owner_id
    )


def delete_questionnaire(db: _orm.Session, research_id: int, id: int, owner_id: int):
    _questionnaireRepo.delete_questionnaire(db, research_id, id, owner_id)


def get_all_question_by_questionnaire(
    db: _orm.Session, questionnaire_id: int, owner_id: int
):
    return _questionRepo.get_all_questions_by_questionnaire(
        db, questionnaire_id, owner_id
    )


def create_question(
    db: _orm.Session,
    question: _schemas.QuestionCreate,
    questionnaire_id: int,
    owner_id: int,
):
    return _questionRepo.create_question(db, question, questionnaire_id, owner_id)


def update_question(
    db: _orm.Session,
    question: _schemas.QuestionCreate,
    questionnaire_id: int,
    id: int,
    owner_id: int,
):
    _questionRepo.update_question(db, question, questionnaire_id, id, owner_id)


def delete_question(db: _orm.Session, questionnaire_id: int, id: int, owner_id: int):
    _questionRepo.delete_question(db, questionnaire_id, id, owner_id)


def get_all_alternatives_by_question(db: _orm.Session, question_id: int, owner_id: int):
    return _alternativeRepo.get_all_alternatives_by_question(db, question_id, owner_id)


def create_alternative(
    db: _orm.Session,
    alternative: _schemas.AlternativeCreate,
    question_id: int,
    owner_id: int,
):
    return _alternativeRepo.create_alternative(db, alternative, question_id, owner_id)


def update_alternative(
    db: _orm.Session,
    alternative: _schemas.AlternativeCreate,
    question_id: int,
    id: int,
    owner_id: int,
):
    _alternativeRepo.update_alternative(db, alternative, question_id, id, owner_id)


def delete_alternative(db: _orm.Session, question_id: int, id: int, owner_id: int):
    _alternativeRepo.delete_alternative(db, question_id, id, owner_id)


def create_access_token(id: str):
    encoded_jwt = _auth.encodeUser(id=id)

    return dict(access_token=encoded_jwt, token_type="bearer")


def authenticate_user(db: _orm.Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        print("username nor found")
        return False
    if not _auth.verify_password(password, user.hashed_password, pwd_context):
        print("incorrect password")
        return False
    return user


def get_current_user(
    db: _orm.Session = _fastapi.Depends(get_db),
    token: str = _fastapi.Depends(oauth2schema),
):
    try:
        payload = _auth.decodeUser(token)
        return _userRepo.get_user(db, payload["id"])
    except:
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid email or password"
        )


def get_public_questionnaires(db: _orm.Session):
    return _questionnaireRepo.get_public_questionnaires(db=db)


def add_questionnaire_templates(
    db: _orm.Session, research_id: int, owner_id: int, ids_list: List[int]
):

    final_questionnaire_list = []
    for original_questionnaire_id in ids_list:
        saved_questionnaire = _questionnaireRepo.add_questionnaires_from_template(
            db=db,
            research_id=research_id,
            owner_id=owner_id,
            original_id=original_questionnaire_id,
        )
        final_questionnaire_list.append(saved_questionnaire)
        original_questions = _questionRepo.get_all_questions_by_questionnaire_template(
            db=db, questionnaire_id=original_questionnaire_id
        )
        for original_question in original_questions:
            saved_question = _questionRepo.add_questions_from_template(
                db=db,
                owner_id=owner_id,
                new_questionnaire_id=saved_questionnaire.id,
                original_question=original_question,
            )
            _alternativeRepo.add_alternative_from_template(
                db=db,
                original_question_id=original_question.id,
                owner_id=owner_id,
                new_question_id=saved_question.id,
            )
    return final_questionnaire_list
