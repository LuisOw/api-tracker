from pydantic import BaseModel, EmailStr
from typing import Optional, Union


class ResearchBase(BaseModel):
    title: str


class ResearchCreate(ResearchBase):
    pass


class Research(ResearchBase):
    id: int

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


class User(UserBase):
    disabled: Union[bool, None] = None

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
