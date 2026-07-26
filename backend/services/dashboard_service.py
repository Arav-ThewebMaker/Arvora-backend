from .progress_service import (
    get_total_study_minutes,
    get_total_sessions,
    get_average_focus,
    get_avg_rating,
    get_avg_session_length,
    get_weekly_sessions,
    get_weekly_minutes,
    get_unique_days,
    get_productive_weekday,
    get_most_studied_subject,
    get_weak_subjects,
    get_performance,
    get_weekly_minutes_graph,
    get_subject_distribution
)
from .study_sessions_service import get_study_sessions
from .streaks_service import calculate_streak
from .exam_readiness_service import get_all_exam_readiness
from .daily_plan_service import generate_daily_plan
from .recommendation_services import get_ranked_exams


def get_dashboard_data(user_id, study_time):
    sessions = get_study_sessions(user_id)

    exams = get_ranked_exams(user_id)

    total_study_minutes = get_total_study_minutes(sessions)
    total_sessions = get_total_sessions(sessions)
    current_streak = calculate_streak(user_id)
    unique_study_days = get_unique_days(sessions)
    weekly_sessions = get_weekly_sessions(sessions)
    weekly_minutes = get_weekly_minutes(sessions)
    avg_focus = get_average_focus(sessions)
    avg_rating = get_avg_rating(sessions)
    avg_session_length = get_avg_session_length(sessions)
    most_studied_subject = get_most_studied_subject(sessions)
    productive_weekday = get_productive_weekday(sessions)
    weak_subjects = get_weak_subjects(user_id)
    daily_plan = generate_daily_plan(exams, study_time)
    exams_readiness = get_all_exam_readiness(user_id)
    weekly_graph = get_weekly_minutes_graph(sessions)
    subject_distribution = get_subject_distribution(sessions)
    performance = get_performance(user_id)

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
        "exams": exams,
        "daily_plan": daily_plan,
        "weekly_graph": weekly_graph,
        "subject_distribution": subject_distribution,

        # Overall performance
        "performance_score": performance
    }

    return dashboard_data
