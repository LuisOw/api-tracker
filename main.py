from typing import List
import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

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


@app.post("/pesquisador", tags=["Conta"])
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
        raise _fastapi.HTTPException(status_code=400, detail="Invalid email")

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


@app.get("/pesquisas", tags=["Pesquisa"], response_model=List[_schemas.Research])
async def get_researches(
    current_user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return _services.get_all_researches_by_user(db, current_user.id)


@app.post("/pesquisas", tags=["Pesquisa"], response_model=_schemas.Research)
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
    try:
        _services.update_research(
            db=db, research=research, owner_id=current_user.id, id=id
        )
    except ValueError:
        raise _fastapi.HTTPException(
            status_code=400,
            detail="Unable to update active or finished researches",
        )


@app.patch(
    "/pesquisas/{id}",
    tags=["Pesquisa"],
    response_model=_schemas.Research,
)
async def set_status(
    current_user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    id: str = None,
):
    return _services.change_research_status(
        db=db, owner_id=current_user.id, research_id=id
    )


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


@app.delete(
    "/admin/pesquisas/{id}",
    status_code=204,
    response_class=_fastapi.Response,
    tags=["Admin"],
)
async def delete_research_admin(
    current_user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    id: str = None,
):
    if current_user.username == "luis@oswaldo.com":
        _services.delete_research_admin(db, current_user.id, id)
    else:
        raise _fastapi.HTTPException(
            status_code=400,
            detail="Unable to update active or finished researches",
        )


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
    try:
        _services.update_questionnaire(
            db, questionnaire, research_id, id, current_user.id
        )
    except ValueError:
        raise _fastapi.HTTPException(
            status_code=400,
            detail="Unable to update 'visibilidade' property from template",
        )


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


@app.post(
    "/pesquisas/{research_id}/questionarios/templates",
    tags=["Questionario"],
    response_model=List[_schemas.Questionnaire],
)
async def post_questionnaires_template(
    current_user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    research_id: str = None,
    ids_list: _schemas.TemplateInput = None,
):
    print(ids_list)
    saved_questionnaires = _services.add_questionnaire_templates(
        db=db,
        research_id=research_id,
        owner_id=current_user.id,
        ids_list=ids_list.selected_ids,
    )

    return saved_questionnaires


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


@app.get(
    "/questionarios",
    tags=["Questionario"],
    response_model=List[_schemas.QuestionnaireTemplate],
)
async def get_public_questionanires(
    current_user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return _services.get_public_questionnaires(db=db)


@app.get(
    "/pesquisas/{id}/arquivo",
    tags=["Pesquisa"],
    response_class=FileResponse,
)
async def download_file(
    current_user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    id: str = None,
):
    return _services.get_file(db=db, research_id=id, owner_id=current_user.id)


@app.post(
    "/dummy/{research_id}/{alternative_id}",
    tags=["Dummy"],
    status_code=204,
    response_class=_fastapi.Response,
)
async def generate_sample_data(
    current_user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    research_id: str = None,
    alternative_id: str = None,
):

    _services.populate_sample_data(
        db=db,
        research_id=research_id,
        alternative_id=alternative_id,
    )


"""
Subject endpoints
"""


@app.post("/participante", tags=["Conta"], response_model=_schemas.SubjectReturn)
async def create_account(
    subject_info: _schemas.SubjectCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    subject = _services.get_subject_by_username(db, subject_info.username)
    if subject:
        raise _fastapi.HTTPException(status_code=400, detail="CPF already in use")

    try:
        subject = _services.create_subject(db, subject_info)
    except Exception as e:
        raise _fastapi.HTTPException(status_code=400, detail="Invalid CPF")

    token_dict = _services.create_access_token(id=subject.id)
    subject_return = _schemas.SubjectReturn(
        username=subject.username,
        chosen_name=subject.chosen_name,
        token_type=token_dict["token_type"],
        access_token=token_dict["access_token"],
    )
    return subject_return


@app.post("/participante/token", tags=["Conta"], response_model=_schemas.SubjectReturn)
async def login(
    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    print(form_data.username, form_data.password)
    subject = _services.authenticate_user(db, form_data.username, form_data.password)
    if not subject:
        raise _fastapi.HTTPException(
            status_code=_fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_dict = _services.create_access_token(id=subject.id)
    subject_return = _schemas.SubjectReturn(
        username=subject.username,
        chosen_name=subject.chosen_name,
        token_type=token_dict["token_type"],
        access_token=token_dict["access_token"],
    )
    return subject_return


@app.get(
    "/participantes/pesquisas",
    tags=["Participante"],
    response_model=List[_schemas.SimplifiedResearch],
)
async def subject_get_researches(
    current_subject: _schemas.SubjectBase = _fastapi.Depends(
        _services.get_current_subject
    ),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return _services.get_all_researches_by_subject(db, current_subject.id)


@app.patch(
    "/participantes/pesquisas/{id}",
    tags=["Participante"],
    status_code=204,
    response_class=_fastapi.Response,
)
async def subject_patch_researches(
    current_subject: _schemas.SubjectBase = _fastapi.Depends(
        _services.get_current_subject
    ),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    id: int = None,
):
    return _services.add_subject_to_research(db, current_subject.id, id)


@app.get(
    "/participantes/pesquisas-filtradas",
    tags=["Participante"],
    response_model=List[_schemas.SimplifiedResearch],
)
async def get_filtered_researches(
    current_subject: _schemas.SubjectBase = _fastapi.Depends(
        _services.get_current_subject
    ),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return _services.get_all_filtered_researches(db=db, subject_id=current_subject.id)


@app.patch(
    "/participantes",
    tags=["Participante"],
    status_code=204,
    response_class=_fastapi.Response,
)
async def patch_subjects(
    current_subject: _schemas.SubjectBase = _fastapi.Depends(
        _services.get_current_subject
    ),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    filter_list: _schemas.FilterList = None,
):
    _services.patch_subject(
        db=db, subject_id=current_subject.id, filter_list=filter_list
    )


@app.get("/participantes", tags=["Participante"], response_model=_schemas.FilterList)
async def get_subject_filters(
    current_subject: _schemas.SubjectBase = _fastapi.Depends(
        _services.get_current_subject
    ),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return _services.get_subject(db=db, subject_id=current_subject.id)


@app.get(
    "/participantes/pesquisas/{id}/questionarios",
    tags=["Participante"],
    response_model=List[_schemas.Questionnaire],
)
async def get_subject_questionnaires(
    current_subject: _schemas.SubjectBase = _fastapi.Depends(
        _services.get_current_subject
    ),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    id: int = None,
):
    return _services.get_subject_related_to_research(
        db=db, subject_id=current_subject.id, research_id=id
    )


@app.get(
    "/participantes/pesquisas/{research_id}/questionarios/{id}/questoes",
    tags=["Participante"],
    response_model=List[_schemas.QuestionTemplate],
)
async def get_subject_questions_and_alternatives(
    current_subject: _schemas.SubjectBase = _fastapi.Depends(
        _services.get_current_subject
    ),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    research_id: int = None,
    id: int = None,
):
    return _services.get_full_question(
        db=db,
        subject_id=current_subject.id,
        research_id=research_id,
        questionnaire_id=id,
    )


@app.post(
    "/participantes/pesquisas/{research_id}/questionarios/{id}/questoes",
    tags=["Respostas"],
    status_code=204,
    response_class=_fastapi.Response,
)
async def post_alternative_answers(
    current_subject: _schemas.User = _fastapi.Depends(_services.get_current_subject),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    research_id: str = None,
    answers: _schemas.AwnserBulkCreate = None,
):
    return _services.post_alternative_answers(
        db=db, subject_id=current_subject.id, research_id=research_id, answers=answers
    )


@app.post(
    "/participantes/uso",
    tags=["Respostas"],
    status_code=204,
    response_class=_fastapi.Response,
)
async def post_usage_time(
    current_subject: _schemas.User = _fastapi.Depends(_services.get_current_subject),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    usage_time: _schemas.UsageTimeCreate = None,
):
    _services.post_usage_time(
        db=db,
        subject_id=current_subject.id,
        usage_time=usage_time,
    )


@app.delete(
    "/participantes",
    tags=["Respostas"],
    status_code=204,
    response_class=_fastapi.Response,
)
async def delete_usage_time_of_user(
    current_user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    _services.delete_usage_time(db=db, subject_id=current_user.id)
