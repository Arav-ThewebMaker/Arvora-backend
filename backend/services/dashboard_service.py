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
    exams = get_ranked_exams(user_id)

    total_study_minutes = get_total_study_minutes(user_id)
    total_sessions = get_total_sessions(user_id)
    current_streak = calculate_streak(user_id)
    unique_study_days = get_unique_days(user_id)
    weekly_sessions = get_weekly_sessions(user_id)
    weekly_minutes = get_weekly_minutes(user_id)
    avg_focus = get_average_focus(user_id)
    avg_rating = get_avg_rating(user_id)
    avg_session_length = get_avg_session_length(user_id)
    most_studied_subject = get_most_studied_subject(user_id)
    productive_weekday = get_productive_weekday(user_id)
    weak_subjects = get_weak_subjects(user_id)
    daily_plan = generate_daily_plan(exams, study_time)
    exams_readiness = get_all_exam_readiness(user_id)
    weekly_graph = get_weekly_minutes_graph(user_id)
    subject_distribution = get_subject_distribution(user_id)
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
