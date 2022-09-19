import datetime
from pydantic import BaseModel
from typing import List, Union


class ResearchBase(BaseModel):
    title: str
    visibility: str
    description: str
    initialAge: Union[int, None] = None
    finalAge: Union[int, None] = None
    initialIncome: Union[int, None] = None
    finalIncome: Union[int, None] = None
    race: Union[str, None] = None
    gender: Union[str, None] = None
    sexualOrientation: Union[str, None] = None


class ResearchCreate(ResearchBase):
    pass


class Research(ResearchBase):
    id: int
    state: str
    code: str
    startTime: Union[datetime.datetime, None] = None
    endTime: Union[datetime.datetime, None] = None

    class Config:
        orm_mode = True


class SimplifiedResearch(BaseModel):
    id: int
    title: str
    description: str
    state: str

    class Config:
        orm_mode = True


class QuestionnaireBase(BaseModel):
    title: str
    public: str


class QuestionnaireCreate(QuestionnaireBase):
    pass


class Questionnaire(QuestionnaireBase):
    id: int

    class Config:
        orm_mode = True


class QuestionBase(BaseModel):
    query: str
    order: int


class QuestionCreate(QuestionBase):
    pass


class Question(QuestionBase):
    id: int

    class Config:
        orm_mode = True


class AlternativeBase(BaseModel):
    type: str
    text: str
    value: int


class AlternativeCreate(AlternativeBase):
    pass


class Alternative(AlternativeBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    full_name: Union[str, None] = None


class SubjectBase(BaseModel):
    username: str
    chosen_name: str


class SubjectReturn(SubjectBase):
    access_token: str
    token_type: str


class User(UserBase):
    disabled: Union[bool, None] = None

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class SubjectCreate(SubjectBase):
    password: str


class UserInDB(User):
    hashed_password: str


class SubjectInDB(SubjectBase):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class QuestionTemplate(Question):
    alternatives: List[Alternative]


class QuestionnaireTemplate(Questionnaire):
    questions: List[QuestionTemplate]

    class Config:
        orm_mode = True


class TemplateInput(BaseModel):
    selected_ids: List[str]


class AnswersBase(BaseModel):
    alternative_chosen: Union[str, None] = None
    text: Union[str, None] = None
    alternative_id: int


class AnswerCreate(AnswersBase):
    pass


class AwnserBulkCreate(BaseModel):
    alternatives: List[AlternativeBase]


class Answers(AnswersBase):
    id: int

    class Config:
        orm_mode = True


class FilterList(BaseModel):
    birth_date: Union[datetime.date, None] = None
    income: Union[int, None] = None
    race: Union[str, None] = None
    gender: Union[str, None] = None
    sexualOrientation: Union[str, None] = None

    class Config:
        orm_mode = True
