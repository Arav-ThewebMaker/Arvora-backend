from .study_sessions_service import get_study_sessions
from .exams_services import get_exams
from .streaks_service import calculate_streak
from datetime import datetime, timedelta


def get_total_study_minutes(sessions):

    total_minutes = 0

    for session in sessions:
        print(session)
        total_minutes += session["minutes"]

    return total_minutes


def get_total_sessions(sessions):

    return len(sessions)


def get_average_focus(sessions):
    if len(sessions) == 0:
        return 0

    total_focus = 0

    for session in sessions:
        total_focus += session["focus"]

    avg_focus = round(total_focus / len(sessions), 2)

    return avg_focus


def get_most_studied_subject(sessions):
    subject_minutes = {}

    top_subject = None
    top_subject_minutes = 0

    for session in sessions:
        subject = session["subject"]
        minutes = session["minutes"]

        if subject in subject_minutes:
            subject_minutes[subject] += minutes
        else:
            subject_minutes[subject] = minutes

        if subject_minutes[subject] > top_subject_minutes:
            top_subject = subject
            top_subject_minutes = subject_minutes[subject]

    return {"subject": top_subject,
            "minutes": top_subject_minutes}


def get_sessions_by_subject(sessions, subject):
    subject_sessions = []

    for session in sessions:
        session_subject = session["subject"]

        if session_subject == subject:
            subject_sessions.append(session)

    return subject_sessions


def get_minutes_for_subject(sessions, subject):
    minutes_for_subject = 0

    subject_sessions = get_sessions_by_subject(sessions, subject)

    for session in subject_sessions:
        minutes_for_subject += session["minutes"]

    return minutes_for_subject


def get_avg_focus_for_subject(sessions, subject):

    subject_sessions = get_sessions_by_subject(
        sessions,
        subject
    )

    if len(subject_sessions) == 0:
        return 0

    total_focus = 0

    for session in subject_sessions:
        total_focus += session["focus"]

    return round(
        total_focus / len(subject_sessions),
        2
    )


def get_weak_subjects(user_id):

    from .exam_readiness_service import get_exam_readiness

    exams = get_exams(user_id)

    subjects = {}

    for exam in exams:

        subject = exam["subject"]

        readiness = get_exam_readiness(
            user_id,
            exam
        )

        if subject not in subjects:
            subjects[subject] = []

        subjects[subject].append(readiness)

    result = []

    for subject, values in subjects.items():

        readiness = round(
            sum(values) / len(values),
            2
        )

        result.append({
            "subject": subject,
            "readiness": readiness,
            "weakness": round(100-readiness, 2)
        })

    result.sort(
        key=lambda x: x["weakness"],
        reverse=True
    )

    return result[:3]


def get_avg_rating(sessions):
    if get_total_sessions(sessions) == 0:
        return 0

    total_rating = 0

    for session in sessions:
        total_rating += session["rating"]

    avg_rating = round(total_rating / get_total_sessions(sessions), 2)

    return avg_rating


def get_weekly_sessions(sessions):
    today = datetime.today().date()

    count = 0

    for session in sessions:
        date = datetime.strptime(session["date"], "%Y-%m-%d").date()
        difference = today - date

        if 0 <= difference.days <= 7:
            count += 1

    return count


def get_weekly_minutes(sessions):
    today = datetime.today().date()

    minutes = 0

    for session in sessions:
        date = datetime.strptime(session["date"], "%Y-%m-%d").date()
        difference = today - date

        if 0 <= difference.days <= 7:
            minutes += session["minutes"]

    return minutes


def get_avg_session_length(sessions):

    if len(sessions) == 0:
        return 0

    total = 0

    for session in sessions:
        total += session["minutes"]

    return round(total / len(sessions))


def get_productive_weekday(sessions):
    days_minutes = {
        "Monday": 0,
        "Tuesday": 0,
        "Wednesday": 0,
        "Thursday": 0,
        "Friday": 0,
        "Saturday": 0,
        "Sunday": 0
    }

    top_day = None
    top_minutes = 0

    for session in sessions:

        day = datetime.strptime(
            session["date"],
            "%Y-%m-%d"
        ).strftime("%A")

        days_minutes[day] += session["minutes"]

        if days_minutes[day] > top_minutes:
            top_day = day
            top_minutes = days_minutes[day]

    return {
        "day": top_day,
        "minutes": top_minutes
    }


def get_unique_days(sessions):
    days = set()

    for session in sessions:
        days.add(session["date"])

    return len(days)


def get_performance(sessions, user_id):

    from .exam_readiness_service import get_all_exam_readiness

    avg_focus = get_average_focus(sessions)
    avg_rating = get_avg_rating(sessions)
    weekly_minutes = get_weekly_minutes(sessions)
    streak = calculate_streak(user_id)

    exams = get_all_exam_readiness(user_id)

    if len(exams) == 0:
        average_readiness = 0
    else:
        total = 0

        for exam in exams:
            total += exam["readiness"]

        average_readiness = round(
            total / len(exams)
        )

    focus_score = avg_focus * 10
    rating_score = avg_rating * 20
    weekly_score = min((weekly_minutes / 600) * 100, 100)
    streak_score = min((streak / 14) * 100, 100)

    score = (
        average_readiness * 0.35 +
        focus_score * 0.20 +
        rating_score * 0.15 +
        streak_score * 0.15 +
        weekly_score * 0.15
    )

    score = round(score, 2)

    if score >= 95:
        grade = "Outstanding"
    elif score >= 85:
        grade = "Excellent"
    elif score >= 75:
        grade = "Very Good"
    elif score >= 65:
        grade = "Good"
    elif score >= 50:
        grade = "Fair"
    else:
        grade = "Needs Improvement"

    return {
        "score": score,
        "grade": grade
    }


def get_weekly_minutes_graph(sessions):
    weekdays = [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun"
    ]

    days = {
        "Mon": 0,
        "Tue": 0,
        "Wed": 0,
        "Thu": 0,
        "Fri": 0,
        "Sat": 0,
        "Sun": 0
    }

    today = datetime.today().date()
    start_of_week = today - timedelta(days=today.weekday())

    for session in sessions:
        date = datetime.strptime(session["date"], "%Y-%m-%d").date()

        if date >= start_of_week:
            weekday = weekdays[date.weekday()]
            days[weekday] += session["minutes"]

    result = []

    for day in days:
        result.append({
            "day": day,
            "minutes": days[day]
        })

    return result


def get_subject_consistency(sessions, subject, days=14):

    subject_sessions = get_sessions_by_subject(
        sessions,
        subject
    )

    today = datetime.today().date()

    start_date = today - timedelta(days=days-1)

    study_days = set()

    for session in subject_sessions:

        session_date = datetime.strptime(
            session["date"],
            "%Y-%m-%d"
        ).date()

        if session_date >= start_date:
            study_days.add(session_date)

    return round(
        len(study_days) / days,
        2
    )


def get_subject_distribution(sessions):
    distribution = {}

    for session in sessions:

        subject = session["subject"]

        if subject not in distribution:
            distribution[subject] = 0

        distribution[subject] += session["minutes"]

    result = []

    for subject, minutes in distribution.items():

        result.append({

            "subject": subject,
            "minutes": minutes

        })

    return result
