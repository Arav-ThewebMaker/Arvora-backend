from .progress_service import (
    get_weak_subjects,
    get_performance,
    get_subject_stats
)
from .dashboard_cache import (
    get_cached_dashboard,
    set_cached_dashboard
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
import time


def get_dashboard_data(user_id, study_time):

    total_start = time.perf_counter()

    def checkpoint(name, start):
        now = time.perf_counter()
        print(f"{name:<30}: {now-start:.4f}s")
        return now

    step = total_start

    cached = get_cached_dashboard(user_id)
    step = checkpoint("Cache check", step)

    if cached:
        print(f"TOTAL (cached): {time.perf_counter()-total_start:.4f}s")
        return cached

    with ThreadPoolExecutor(max_workers=2) as executor:

        sessions_future = executor.submit(
            get_study_sessions,
            user_id
        )

        exams_future = executor.submit(
            get_exams,
            user_id
        )

        sessions = sessions_future.result()
        exams = exams_future.result()

    ranked_exams = get_ranked_exams(exams)

    step = checkpoint("Fetch sessions + exams", step)

    for session in sessions:
        session["parsed_date"] = datetime.strptime(
            session["date"],
            "%Y-%m-%d"
        ).date()

    step = checkpoint("Parse dates", step)

    subject_stats = get_subject_stats(sessions)
    step = checkpoint("Subject stats", step)

    stats = calculate_dashboard_stats(sessions)
    step = checkpoint("Dashboard stats", step)

    current_streak = calculate_streak(sessions)
    step = checkpoint("Current streak", step)

    weak_subjects = get_weak_subjects(
        ranked_exams,
        subject_stats
    )
    step = checkpoint("Weak subjects", step)

    daily_plan = generate_daily_plan(
        ranked_exams,
        study_time
    )
    step = checkpoint("Daily plan", step)

    exams_readiness = get_all_exam_readiness(
        ranked_exams,
        subject_stats
    )
    step = checkpoint("Exam readiness", step)

    performance = get_performance(
        sessions,
        exams_readiness,
        current_streak
    )
    step = checkpoint("Performance", step)

    dashboard_data = {
        "total_study_minutes": stats["total_study_minutes"],
        "total_sessions": stats["total_sessions"],
        "unique_study_days": stats["unique_study_days"],
        "current_streak": current_streak,

        "weekly_sessions": stats["weekly_sessions"],
        "weekly_minutes": stats["weekly_minutes"],

        "average_focus": stats["average_focus"],
        "average_rating": stats["average_rating"],
        "average_session_length": stats["average_session_length"],

        "most_studied_subject": stats["most_studied_subject"],
        "productive_weekday": stats["productive_weekday"],

        "weak_subjects": weak_subjects,
        "exams_readiness": exams_readiness,

        "exams": ranked_exams,
        "daily_plan": daily_plan,
        "weekly_graph": stats["weekly_graph"],
        "subject_distribution": stats["subject_distribution"],

        "performance_score": performance
    }

    set_cached_dashboard(
        user_id,
        dashboard_data
    )
    step = checkpoint("Cache save", step)

    print("=" * 60)
    print(f"TOTAL DASHBOARD TIME: {time.perf_counter()-total_start:.4f}s")
    print("=" * 60)

    return dashboard_data
