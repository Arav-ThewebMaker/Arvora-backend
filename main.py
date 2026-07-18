from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.models.exam_model import ExamCreate
from backend.services.dashboard_service import get_dashboard_data
from backend.services.exams_services import add_exam, delete_exam, update_exam
from backend.models.study_session_model import StudySessionCreate
from backend.services.study_sessions_service import record_study_session, get_study_sessions, delete_study_session, update_study_session as update_sessions
from backend.services.recommendation_services import get_ranked_exams
from backend.models.auth_models import UserRegister
from backend.models.auth_models import UserLogin
from backend.services.auth_service import register_user
from backend.services.auth_service import login_user
from backend.services.auth_dependency import get_current_user


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/dashboard")
def return_dashboard_data(
    study_time: int = 60,
    user=Depends(get_current_user)
):
    return get_dashboard_data(user["user_id"], study_time)


@app.get("/exams")
def fetch_exams(
    user=Depends(get_current_user)
):
    user_id = user["user_id"]
    return get_ranked_exams(user_id)


@app.post("/exams")
def create_exam(
    exam: ExamCreate,
    user=Depends(get_current_user)
):

    user_id = user["user_id"]

    add_exam(
        user_id,
        exam.subject,
        exam.date,
        exam.target_percentage,
        exam.current_percentage,
        exam.importance
    )

    return {"status": "exam created"}


@app.get("/study-session")
def fetch_study_sessions(user=Depends(get_current_user)):

    return get_study_sessions(user["user_id"])


@app.post("/study-session")
def create_study_session(
    session: StudySessionCreate,
    user=Depends(get_current_user)
):

    user_id = user["user_id"]

    record_study_session(
        user_id,
        session.subject,
        session.date,
        session.minutes,
        session.focus,
        session.study_method,
        session.rating,
        session.chapter_name
    )

    return {"status": "study session added"}


@app.delete("/study-session/{session_id}")
def remove_study_session(
    session_id: int,
    user=Depends(get_current_user)
):

    user_id = user["user_id"]
    return delete_study_session(session_id, user_id)


@app.put("/study-session/{session_id}")
def update_study_session(
    session_id: int,
    session: StudySessionCreate,
    user=Depends(get_current_user)
):

    user_id = user["user_id"]
    return update_sessions(
        session_id,
        user_id,
        session.subject,
        session.date,
        session.minutes,
        session.focus,
        session.study_method,
        session.rating,
        session.chapter_name)


@app.post("/register")
def register(user: UserRegister):

    result = register_user(
        user.username,
        user.password
    )

    if result["status"] == "error":
        raise HTTPException(
            status_code=400,
            detail=result["message"]
        )

    return result


@app.post("/login")
def login(user: UserLogin):

    return login_user(
        user.username,
        user.password
    )


@app.delete("/exams/{exam_id}")
def remove_exam(
    exam_id: int,
    user=Depends(get_current_user)
):
    user_id = user["user_id"]
    return delete_exam(user_id, exam_id)


@app.put("/exams/{exam_id}")
def edit_exam(
    exam_id: int,
    exam: ExamCreate,
    user=Depends(get_current_user)
):
    user_id = user["user_id"]

    return update_exam(
        user_id,
        exam_id,
        exam.subject,
        exam.target_percentage,
        exam.current_percentage,
        exam.importance
    )
