from datetime import datetime


def calculate_exam_urgency(exam):
    if not exam["date"]:
        return 0

    if isinstance(exam["date"], str):
        exam_date = datetime.strptime(
            exam["date"],
            "%Y-%m-%d"
        ).date()
    else:
        exam_date = exam["date"]

    today = datetime.today().date()

    days_left = (exam_date - today).days
    if days_left < 0:
        days_left = 0

    target = exam.get("target_percentage") or 0
    current = exam.get("current_percentage") or 0

    gap = target - current

    time_pressure = 100 / (days_left + 1)

    importance_score = ((exam["importance"] / 5) * 100)
    gap_score = ((gap / 100) * 100)
    time_pressure_score = min(time_pressure, 100)

    urgency = round(importance_score * 0.4 + gap_score *
                    0.3 + time_pressure_score * 0.3, 2)

    return urgency


def get_ranked_exams(exams):

    for exam in exams:
        exam["urgency"] = calculate_exam_urgency(exam)

    exams.sort(key=lambda x: x["urgency"], reverse=True)

    return exams
