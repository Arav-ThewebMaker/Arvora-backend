def merge_exam_subjects(exams):
    merged = {}

    for exam in exams:
        subject = exam["subject"]

        if subject not in merged:
            merged[subject] = {
                "subject": subject,
                "urgency": exam["urgency"],
                "minutes": 0,
                "exams": []
            }

        # Add all exams of same subject together
        merged[subject]["minutes"] += 30
        merged[subject]["exams"].append(exam)

        # Keep highest urgency among same subject exams
        if exam["urgency"] > merged[subject]["urgency"]:
            merged[subject]["urgency"] = exam["urgency"]

    return list(merged.values())


def generate_daily_plan(exams, study_time):

    if not exams:
        return []

    # Merge same subjects
    exams = merge_exam_subjects(exams)

    # Sort by urgency
    exams.sort(
        key=lambda x: x["urgency"],
        reverse=True
    )

    plan = []

    remaining_time = study_time

    for exam in exams:

        if remaining_time <= 0:
            break

        # Allocate time based on urgency
        urgency_ratio = exam["urgency"] / 100

        allocated = round(
            study_time * urgency_ratio
        )

        # Minimum 15 minutes
        if allocated < 15:
            allocated = 15

        # Don't exceed remaining time
        allocated = min(
            allocated,
            remaining_time
        )

        plan.append({
            "subject": exam["subject"],
            "minutes": allocated,
            "urgency": exam["urgency"],
            "exam_count": len(exam["exams"])
        })

        remaining_time -= allocated

    # If time remains, add it to highest priority subject
    if remaining_time > 0 and len(plan) > 0:

        plan[0]["minutes"] += remaining_time

    return plan
