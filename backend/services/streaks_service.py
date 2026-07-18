from .study_sessions_service import get_study_sessions
from datetime import datetime, timedelta


def calculate_streak(user_id):
    sessions = get_study_sessions(user_id)

    if not sessions:
        return 0

    dates = {
        datetime.strptime(session["date"], "%Y-%m-%d").date()
        for session in sessions
    }

    dates = sorted(dates)

    streak = 1

    for i in range(len(dates) - 1, 0, -1):
        if dates[i] - dates[i - 1] == timedelta(days=1):
            streak += 1
        else:
            break

    return streak
