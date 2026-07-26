from db_pool import pool
from psycopg.rows import dict_row


def add_subject(user_id, name, priority):

    with pool.connection() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                INSERT INTO subjects (
                    user_id,
                    name,
                    priority
                )
                VALUES (%s, %s, %s)
            """, (
                user_id,
                name,
                priority
            ))

            conn.commit()

    return {
        "status": "success"
    }


def get_subjects(user_id):

    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute("""
                SELECT id, name, priority
                FROM subjects
                WHERE user_id = %s
            """, (
                user_id,
            ))

            return cur.fetchall()
