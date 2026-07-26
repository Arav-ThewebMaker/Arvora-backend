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

    today = datetime.today().date()

    # If user didn't study today, allow yesterday.
    if today in dates:
        current = today
    elif (today - timedelta(days=1)) in dates:
        current = today - timedelta(days=1)
    else:
        return 0

    streak = 0

    while current in dates:
        streak += 1
        current -= timedelta(days=1)

    return streak
