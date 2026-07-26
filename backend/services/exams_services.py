from database import connect
from datetime import datetime


def add_exam(user_id, subject, date, target_percentage, current_percentage, importance):

    if not subject or subject.strip() == "":
        return {
            "status": "error",
            "message": "Subject is required"
        }

    exam_date = datetime.strptime(date, "%Y-%m-%d").date()
    today = datetime.today().date()

    if exam_date < today:
        return {
            "status": "error",
            "message": "Exam date cannot be in the past"
        }

    conn = connect()
    cur = conn.cursor()

    if importance is None or importance == "":
        importance = 3

    cur.execute("""
        INSERT INTO exams (
            user_id,
            subject,
            date,
            target_percentage,
            current_percentage,
            importance
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        user_id,
        subject,
        date,
        target_percentage,
        current_percentage,
        importance
    ))

    conn.commit()
    cur.close()
    conn.close()

    return {
        "status": "success"
    }


def get_exams(user_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT id,
               user_id,
               subject,
               date,
               target_percentage,
               current_percentage,
               importance
        FROM exams
        WHERE user_id = %s
    """, (user_id,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    exams = []

    for r in rows:
        exams.append({
            "id": r[0],
            "user_id": r[1],
            "subject": r[2],
            "date": str(r[3]),
            "target_percentage": r[4],
            "current_percentage": r[5],
            "importance": r[6]
        })

    return exams


def delete_exam(user_id, exam_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM exams
        WHERE id = %s AND user_id = %s
    """, (exam_id, user_id))

    conn.commit()

    cur.close()
    conn.close()

    return {"status": "deleted"}


def update_exam(
    user_id,
    exam_id,
    subject,
    target_percentage,
    current_percentage,
    importance
):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        UPDATE exams
        SET subject = %s,
            target_percentage = %s,
            current_percentage = %s,
            importance = %s
        WHERE id = %s
          AND user_id = %s
    """, (
        subject,
        target_percentage,
        current_percentage,
        importance,
        exam_id,
        user_id
    ))

    conn.commit()

    cur.close()
    conn.close()

    return {"status": "updated"}
