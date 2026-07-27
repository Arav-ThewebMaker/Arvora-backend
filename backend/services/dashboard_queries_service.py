from db_pool import pool


def get_dashboard_stats(user_id):

    with pool.connection() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                SELECT
                    COUNT(*) AS total_sessions,
                    COALESCE(SUM(minutes),0) AS total_study_minutes,
                    COUNT(DISTINCT date) AS unique_study_days,

                    COALESCE(AVG(focus),0) AS average_focus,
                    COALESCE(AVG(rating),0) AS average_rating,
                    COALESCE(AVG(minutes),0) AS average_session_length

                FROM study_sessions
                WHERE user_id=%s
            """, (user_id,))

            row = cur.fetchone()

    return {
        "total_sessions": row[0],
        "total_study_minutes": row[1],
        "unique_study_days": row[2],
        "average_focus": round(row[3], 2),
        "average_rating": round(row[4], 2),
        "average_session_length": round(row[5], 2)
    }
