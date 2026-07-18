from .study_sessions_service import get_study_sessions
from .exams_services import get_exams
from .streaks_service import calculate_streak
from datetime import datetime, timedelta


def get_total_study_minutes(user_id):
    sessions = get_study_sessions(user_id)

    total_minutes = 0

    for session in sessions:
        print(session)
        total_minutes += session["minutes"]

    return total_minutes


def get_total_sessions(user_id):
    sessions = get_study_sessions(user_id)

    return len(sessions)


def get_average_focus(user_id):
    sessions = get_study_sessions(user_id)

    if get_total_sessions(user_id) == 0:
        return 0

    total_focus = 0

    for session in sessions:
        total_focus += session["focus"]

    avg_focus = round(total_focus/get_total_sessions(user_id), 2)

    return avg_focus


def get_most_studied_subject(user_id):
    sessions = get_study_sessions(user_id)

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


def get_sessions_by_subject(user_id, subject):
    sessions = get_study_sessions(user_id)

    subject_sessions = []

    for session in sessions:
        session_subject = session["subject"]

        if session_subject == subject:
            subject_sessions.append(session)

    return subject_sessions


def get_minutes_for_subject(user_id, subject):
    sessions = get_study_sessions(user_id)

    minutes_for_subject = 0

    subject_sessions = get_sessions_by_subject(user_id, subject)

    for session in subject_sessions:
        minutes_for_subject += session["minutes"]

    return minutes_for_subject


def get_avg_focus_for_subject(user_id, subject):
    total_focus = 0

    subject_sessions = get_sessions_by_subject(user_id, subject)

    if len(subject_sessions) == 0:
        return 0

    for session in subject_sessions:
        total_focus += session["focus"]

    avg_focus = total_focus / len(subject_sessions)

    return avg_focus


def get_weak_subjects(user_id):
    from .exam_readiness_service import get_exam_readiness

    exams = get_exams(user_id)

    weakness_exams = []

    for exam in exams:
        exam_readiness = get_exam_readiness(user_id, exam)

        weakness = 100 - exam_readiness

        result = {
            "subject": exam["subject"],
            "weakness": weakness,
            "readiness": exam_readiness
        }
        weakness_exams.append(result)

    weakness_exams.sort(
        key=lambda x: x["weakness"], reverse=True)

    return weakness_exams[:3]


def get_avg_rating(user_id):
    sessions = get_study_sessions(user_id)

    if get_total_sessions(user_id) == 0:
        return 0

    total_rating = 0

    for session in sessions:
        total_rating += session["rating"]

    avg_rating = round(total_rating / get_total_sessions(user_id), 2)

    return avg_rating


def get_weekly_sessions(user_id):
    sessions = get_study_sessions(user_id)

    today = datetime.today().date()

    count = 0

    for session in sessions:
        date = datetime.strptime(session["date"], "%Y-%m-%d").date()
        difference = today - date

        if 0 <= difference.days <= 7:
            count += 1

    return count


def get_weekly_minutes(user_id):
    sessions = get_study_sessions(user_id)

    today = datetime.today().date()

    minutes = 0

    for session in sessions:
        date = datetime.strptime(session["date"], "%Y-%m-%d").date()
        difference = today - date

        if 0 <= difference.days <= 7:
            minutes += session["minutes"]

    return minutes


def get_avg_session_length(user_id):

    if get_total_sessions(user_id) == 0:
        return 0

    avg_session_length = round(get_total_study_minutes(
        user_id) / get_total_sessions(user_id))

    return avg_session_length


def get_productive_weekday(user_id):
    sessions = get_study_sessions(user_id)

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


def get_unique_days(user_id):
    sessions = get_study_sessions(user_id)

    days = set()

    for session in sessions:
        days.add(session["date"])

    return len(days)


def get_performance(user_id):
    from .exam_readiness_service import get_all_exam_readiness

    avg_focus = get_average_focus(user_id)  # 1-10
    avg_rating = get_avg_rating(user_id)  # 1-5
    weekly_minutes = get_weekly_minutes(user_id)  # 0-600
    streak = calculate_streak(user_id)  # 1-14
    exams = get_all_exam_readiness(user_id)

    average_readiness = 0

    if len(exams) == 0:
        average_readiness = 0
    else:
        total = 0

        for exam in exams:
            total += exam["readiness"]

        average_readiness = round(total / len(exams))

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


def get_weekly_minutes_graph(user_id):
    sessions = get_study_sessions(user_id)

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


def get_subject_consistency(user_id, subject, days=14):
    subject_sessions = get_sessions_by_subject(user_id, subject)

    today = datetime.today().date()
    start_date = today - timedelta(days=days - 1)

    study_days = set()

    for session in subject_sessions:
        session_date = datetime.strptime(
            session["date"],
            "%Y-%m-%d"
        ).date()

        if session_date >= start_date:
            study_days.add(session_date)

    return len(study_days) / days


def get_subject_distribution(user_id):

    sessions = get_study_sessions(user_id)

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
