from .recommendation_services import get_ranked_exams


def generate_daily_plan(exams, study_time):
    total_urgency = sum(exam["urgency"] for exam in exams)

    if total_urgency == 0:
        return []

    plan = []

    for exam in exams:
        share = exam["urgency"] / total_urgency
        allocated_minutes = round(share * study_time)

        plan.append({
            "subject": exam["subject"],
            "minutes": allocated_minutes,
            "urgency": exam["urgency"]
        })

    return plan
