from db_pool import pool
from psycopg.rows import dict_row


def record_study_session(
    user_id,
    subject,
    date,
    minutes,
    focus,
    study_method,
    rating,
    chapter_name=None
):

    if not subject or subject.strip() == "":
        return {
            "status": "error",
            "message": "Subject is required"
        }

    with pool.connection() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                INSERT INTO study_sessions (
                    user_id,
                    subject,
                    chapter_name,
                    date,
                    minutes,
                    focus,
                    method,
                    rating
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                user_id,
                subject,
                chapter_name,
                date,
                minutes,
                focus,
                study_method,
                rating
            ))

            conn.commit()

    return {
        "status": "success"
    }


def get_study_sessions(user_id):

    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute("""
            SELECT 
                id,
                user_id,
                subject,
                chapter_name,
                date,
                minutes,
                focus,
                method,
                rating
                FROM study_sessions
                WHERE user_id = %s
                ORDER BY date DESC
            """, (
                user_id,
            ))

            sessions = cur.fetchall()

    for session in sessions:
        session["date"] = str(session["date"])

    return sessions


def delete_study_session(session_id, user_id):

    with pool.connection() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                DELETE FROM study_sessions
                WHERE id = %s
                AND user_id = %s
            """, (
                session_id,
                user_id
            ))

            deleted = cur.rowcount

            conn.commit()

    return {
        "status": "deleted",
        "Rows deleted": deleted
    }


def update_study_session(
    session_id,
    user_id,
    subject,
    date,
    study_time,
    focus,
    method,
    rating,
    chapter_name
):

    with pool.connection() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                UPDATE study_sessions
                SET subject = %s,
                    date = %s,
                    minutes = %s,
                    focus = %s,
                    method = %s,
                    rating = %s,
                    chapter_name = %s
                WHERE id = %s
                AND user_id = %s
            """, (
                subject,
                date,
                study_time,
                focus,
                method,
                rating,
                chapter_name,
                session_id,
                user_id
            ))

            conn.commit()

    return {
        "status": "updated"
    }
