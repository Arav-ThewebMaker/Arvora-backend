from .progress_service import (
    get_weak_subjects,
    get_performance,
)
from .dashboard_stats_service import calculate_dashboard_stats
from concurrent.futures import ThreadPoolExecutor
from .study_sessions_service import get_study_sessions
from .streaks_service import calculate_streak
from .exam_readiness_service import get_all_exam_readiness
from .daily_plan_service import generate_daily_plan
from .recommendation_services import get_ranked_exams
from .exams_services import get_exams
from datetime import datetime


def get_dashboard_data(user_id, study_time):
    sessions = get_study_sessions(user_id)

    from .progress_service import get_subject_stats

    subject_stats = get_subject_stats(sessions)

    with ThreadPoolExecutor() as executor:
        sessions_future = executor.submit(get_study_sessions, user_id)
        exams_future = executor.submit(get_exams, user_id)

        sessions = sessions_future.result()
        exams = exams_future.result()

    for session in sessions:
        session["parsed_date"] = datetime.strptime(
            session["date"],
            "%Y-%m-%d"
        ).date()

    stats = calculate_dashboard_stats(sessions)

    ranked_exams = get_ranked_exams(exams)

    current_streak = calculate_streak(sessions)
    weak_subjects = get_weak_subjects(
        ranked_exams,
        subject_stats
    )
    daily_plan = generate_daily_plan(
        ranked_exams,
        study_time
    )
    exams_readiness = get_all_exam_readiness(
        ranked_exams,
        subject_stats
    )
    performance = get_performance(
        sessions,
        exams_readiness,
        current_streak
    )

    total_study_minutes = stats["total_study_minutes"]

    total_sessions = stats["total_sessions"]

    weekly_sessions = stats["weekly_sessions"]

    weekly_minutes = stats["weekly_minutes"]

    unique_study_days = stats["unique_study_days"]

    avg_focus = stats["average_focus"]

    avg_rating = stats["average_rating"]

    avg_session_length = stats["average_session_length"]

    most_studied_subject = stats["most_studied_subject"]

    productive_weekday = stats["productive_weekday"]

    weekly_graph = stats["weekly_graph"]

    subject_distribution = stats["subject_distribution"]

    dashboard_data = {
        # Overall statistics
        "total_study_minutes": total_study_minutes,
        "total_sessions": total_sessions,
        "unique_study_days": unique_study_days,
        "current_streak": current_streak,

        # Weekly statistics
        "weekly_sessions": weekly_sessions,
        "weekly_minutes": weekly_minutes,

        # Performance statistics
        "average_focus": avg_focus,
        "average_rating": avg_rating,
        "average_session_length": avg_session_length,

        # Subject statistics
        "most_studied_subject": most_studied_subject,
        "productive_weekday": productive_weekday,

        # Study recommendations
        "weak_subjects": weak_subjects,
        "exams_readiness": exams_readiness,

        # Dashboard widgets
        "exams": ranked_exams,
        "daily_plan": daily_plan,
        "weekly_graph": weekly_graph,
        "subject_distribution": subject_distribution,

        # Overall performance
        "performance_score": performance
    }

    return dashboard_data
