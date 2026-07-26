from db_pool import pool
from datetime import datetime
from psycopg.rows import dict_row


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

    with pool.connection() as conn:
        with conn.cursor() as cur:

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

    return {
        "status": "success"
    }


def get_exams(user_id):

    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(
                """
                SELECT *
                FROM exams
                WHERE user_id = %s
                ORDER BY date ASC
                """,
                (user_id,)
            )

            rows = cur.fetchall()

    for exam in rows:
        exam["date"] = str(exam["date"])

    return rows


def delete_exam(user_id, exam_id):

    with pool.connection() as conn:
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM exams
            WHERE id = %s AND user_id = %s
        """, (exam_id, user_id))

        conn.commit()

    return {"status": "deleted"}


def update_exam(
    user_id,
    exam_id,
    subject,
    target_percentage,
    current_percentage,
    importance
):

    with pool.connection() as conn:
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

    return {"status": "updated"}
