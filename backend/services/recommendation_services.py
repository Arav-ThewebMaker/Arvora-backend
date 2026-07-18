from database import connect
from datetime import datetime


def calculate_exam_urgency(exam):
    if not exam["date"]:
        return 0

    exam_date = datetime.strptime(
        exam["date"],
        "%Y-%m-%d"
    )

    today = datetime.now()

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


def get_ranked_exams(user_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM exams WHERE user_id = ?", (user_id, ))
    rows = cur.fetchall()
    conn.close()

    exams = []
    for r in rows:
        exam = {
            "id": r[0],
            "user_id": r[1],
            "subject": r[2],
            "date": r[3],
            "target_percentage": r[4],
            "current_percentage": r[5],
            "importance": r[6]
        }

        exam["urgency"] = calculate_exam_urgency(exam)
        exams.append(exam)

    exams.sort(key=lambda x: x["urgency"], reverse=True)

    return exams
