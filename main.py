import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm
from fastapi.middleware.cors import CORSMiddleware

import schemas as _schemas
import services as _services

app = _fastapi.FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def home():
    return {"hello": "olleh"}


@app.post("/create", tags=["Conta"])
async def create_account(
    user_info: _schemas.UserCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    user = _services.get_user_by_username(db, user_info.username)
    if user:
        raise _fastapi.HTTPException(status_code=400, detail="Email already in use")

    try:
        user = _services.create_user(db, user_info)
    except Exception as e:
        raise _fastapi.HTTPException(status_code=40, detail="Invalid email")

    return _services.create_access_token(id=user.id)


@app.post("/token", tags=["Conta"])
async def login(
    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    print(form_data.username, form_data.password)
    user = _services.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise _fastapi.HTTPException(
            status_code=_fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return _services.create_access_token(id=user.id)


@app.get("/pesquisas", tags=["Pesquisa"])
async def get_researches(
    current_user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return _services.get_all_researches_by_user(db, current_user.id)


@app.post("/pesquisas", tags=["Pesquisa"])
async def post_research(
    current_user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    research: _schemas.ResearchCreate = None,
):
    return _services.create_research(db, research, current_user.id)


@app.put(
    "/pesquisas/{id}",
    status_code=204,
    response_class=_fastapi.Response,
    tags=["Pesquisa"],
)
async def put_research(
    current_user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    research: _schemas.ResearchCreate = None,
    id: str = None,
):
    _services.update_research(db, research, current_user.id, id)


@app.delete(
    "/pesquisas/{id}",
    status_code=204,
    response_class=_fastapi.Response,
    tags=["Pesquisa"],
)
async def delete_research(
    current_user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    id: str = None,
):
    _services.delete_research(db, current_user.id, id)


@app.get("/pesquisas/{research_id}/questionarios", tags=["Questionario"])
async def get_questionnaires(
    current_user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    research_id: str = None,
):
    return _services.get_all_questionnaires_by_research(
        db, research_id, current_user.id
    )


@app.post("/pesquisas/{research_id}/questionarios", tags=["Questionario"])
async def post_questionnaire(
    current_user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    research_id: str = None,
    questionnaire: _schemas.QuestionnaireCreate = None,
):
    return _services.create_questionnaire(
        db, questionnaire, research_id, current_user.id
    )


@app.put(
    "/pesquisas/{research_id}/questionarios/{id}",
    status_code=204,
    response_class=_fastapi.Response,
    tags=["Questionario"],
)
async def put_questionnaire(
    current_user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    questionnaire: _schemas.QuestionnaireCreate = None,
    research_id: str = None,
    id: str = None,
):
    _services.update_questionnaire(db, questionnaire, research_id, id, current_user.id)


@app.delete(
    "/pesquisas/{research_id}/questionarios/{id}",
    status_code=204,
    response_class=_fastapi.Response,
    tags=["Questionario"],
)
async def delete_questionnaire(
    current_user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    research_id: str = None,
    id: str = None,
):
    _services.delete_questionnaire(db, research_id, id, current_user.id)


@app.get(
    "/pesquisas/{research_id}/questionarios/{questionnaire_id}/questoes",
    tags=["Questão"],
)
async def get_questions(
    current_user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    research_id: str = None,
    questionnaire_id: str = None,
):
    return _services.get_all_question_by_questionnaire(
        db, questionnaire_id, current_user.id
    )


@app.post(
    "/pesquisas/{research_id}/questionarios/{questionnaire_id}/questoes",
    tags=["Questão"],
)
async def post_question(
    current_user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    research_id: str = None,
    questionnaire_id: str = None,
    question: _schemas.QuestionCreate = None,
):
    return _services.create_question(db, question, questionnaire_id, current_user.id)


@app.put(
    "/pesquisas/{research_id}/questionarios/{questionnaire_id}/questoes/{id}",
    status_code=204,
    response_class=_fastapi.Response,
    tags=["Questão"],
)
async def put_question(
    current_user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    question: _schemas.QuestionCreate = None,
    questionnaire_id: str = None,
    id: str = None,
):
    _services.update_question(db, question, questionnaire_id, id, current_user.id)


@app.delete(
    "/pesquisas/{research_id}/questionarios/{questionnaire_id}/questoes/{id}",
    status_code=204,
    response_class=_fastapi.Response,
    tags=["Questão"],
)
async def delete_question(
    current_user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    questionnaire_id: str = None,
    id: str = None,
):
    _services.delete_question(db, questionnaire_id, id, current_user.id)


@app.get(
    "/pesquisas/{research_id}/questionarios/{questionnaire_id}/questoes/{question_id}/alternativas",
    tags=["Alternativa"],
)
async def get_questions(
    current_user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    question_id: str = None,
):
    return _services.get_all_alternatives_by_question(db, question_id, current_user.id)


@app.post(
    "/pesquisas/{research_id}/questionarios/{questionnaire_id}/questoes/{question_id}/alternativas",
    tags=["Alternativa"],
)
async def post_alternative(
    current_user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    question_id: str = None,
    alternative: _schemas.AlternativeCreate = None,
):
    return _services.create_alternative(db, alternative, question_id, current_user.id)


@app.put(
    "/pesquisas/{research_id}/questionarios/{questionnaire_id}/questoes/{question_id}/alternativas/{id}",
    status_code=204,
    response_class=_fastapi.Response,
    tags=["Alternativa"],
)
async def put_alternative(
    current_user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    alternative: _schemas.AlternativeCreate = None,
    question_id: str = None,
    id: str = None,
):
    _services.update_alternative(db, alternative, question_id, id, current_user.id)


@app.delete(
    "/pesquisas/{research_id}/questionarios/{questionnaire_id}/questoes/{question_id}/alternativas/{id}",
    status_code=204,
    response_class=_fastapi.Response,
    tags=["Alternativa"],
)
async def delete_question(
    current_user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    question_id: str = None,
    id: str = None,
):
    _services.delete_alternative(db, question_id, id, current_user.id)
