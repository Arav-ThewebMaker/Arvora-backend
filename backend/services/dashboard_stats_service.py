from datetime import datetime, timedelta


def calculate_dashboard_stats(sessions):

    today = datetime.today().date()
    start_of_week = today - timedelta(days=today.weekday())

    total_minutes = 0
    total_focus = 0
    total_rating = 0

    weekly_minutes = 0
    weekly_sessions = 0

    unique_days = set()

    subject_minutes = {}
    subject_distribution = {}

    weekday_minutes = {
        "Monday": 0,
        "Tuesday": 0,
        "Wednesday": 0,
        "Thursday": 0,
        "Friday": 0,
        "Saturday": 0,
        "Sunday": 0
    }

    for session in sessions:

        minutes = session["minutes"]
        focus = session["focus"]
        rating = session["rating"]
        subject = session["subject"]

        date = session["parsed_date"]

        total_minutes += minutes
        total_focus += focus
        total_rating += rating

        unique_days.add(date)

        if date >= start_of_week:
            weekly_minutes += minutes
            weekly_sessions += 1

        weekday = date.strftime("%A")
        weekday_minutes[weekday] += minutes

        subject_minutes[subject] = subject_minutes.get(subject, 0) + minutes
        subject_distribution[subject] = subject_distribution.get(
            subject, 0) + minutes

    total_sessions = len(sessions)

    average_focus = (
        round(total_focus / total_sessions, 2)
        if total_sessions else 0
    )

    average_rating = (
        round(total_rating / total_sessions, 2)
        if total_sessions else 0
    )

    average_session_length = (
        round(total_minutes / total_sessions)
        if total_sessions else 0
    )

    if subject_minutes:
        top_subject = max(
            subject_minutes,
            key=subject_minutes.get
        )

        most_studied_subject = {
            "subject": top_subject,
            "minutes": subject_minutes[top_subject]
        }

    else:

        most_studied_subject = {
            "subject": None,
            "minutes": 0
        }

    productive_day = max(
        weekday_minutes,
        key=weekday_minutes.get
    )

    productive_weekday = {
        "day": productive_day,
        "minutes": weekday_minutes[productive_day]
    }

    weekly_graph = []

    weekdays = [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun"
    ]

    graph = dict.fromkeys(weekdays, 0)

    for session in sessions:

        date = session["parsed_date"]

        if date >= start_of_week:
            graph[weekdays[date.weekday()]] += session["minutes"]

    for day in weekdays:
        weekly_graph.append({
            "day": day,
            "minutes": graph[day]
        })

    distribution = []

    for subject, minutes in subject_distribution.items():
        distribution.append({
            "subject": subject,
            "minutes": minutes
        })

    return {

        "total_study_minutes": total_minutes,

        "total_sessions": total_sessions,

        "average_focus": average_focus,

        "average_rating": average_rating,

        "average_session_length": average_session_length,

        "weekly_minutes": weekly_minutes,

        "weekly_sessions": weekly_sessions,

        "unique_study_days": len(unique_days),

        "most_studied_subject": most_studied_subject,

        "productive_weekday": productive_weekday,

        "weekly_graph": weekly_graph,

        "subject_distribution": distribution

    }
