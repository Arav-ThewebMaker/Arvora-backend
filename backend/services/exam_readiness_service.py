from .progress_service import (
    get_subject_stats
)

from .study_sessions_service import get_study_sessions
from .exams_services import get_exams


def get_required_minutes(target_percentage):

    target_percentage = max(40, min(target_percentage, 100))

    x = (target_percentage - 40) / 60

    return round(400 + 2700 * (x ** 1.4))


def get_exam_readiness(stats, exam):

    subject = exam["subject"]

    subject_stats = stats.get(subject)

    if subject_stats:
        total_minutes = subject_stats["minutes"]

        avg_focus = (
            subject_stats["focus_total"] /
            subject_stats["focus_count"]
        )

        consistency = len(subject_stats["days"]) / 14
    else:
        total_minutes = 0
        avg_focus = 0
        consistency = 0

    required_minutes = get_required_minutes(
        exam["target_percentage"]
    )

    study_progress = min(
        total_minutes / required_minutes,
        1.0
    )

    focus_score = (avg_focus / 10) ** 1.75

    readiness = round(
        (
            study_progress * 0.60 +
            focus_score * 0.15 +
            consistency * 0.25
        ) * 100,
        2
    )

    return readiness


def get_all_exam_readiness(user_id, subject_stats):

    exams = get_exams(user_id)

    exams_readiness = []

    for exam in exams:

        exams_readiness.append({

            "subject": exam["subject"],
            "date": exam["date"],
            "readiness": get_exam_readiness(
                subject_stats,
                exam
            )

        })

    return exams_readiness
