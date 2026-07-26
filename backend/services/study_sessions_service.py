from database import connect


def record_study_session(user_id, subject, date, minutes, focus, study_method, rating, chapter_name=None):
    conn = connect()
    cur = conn.cursor()

    if not subject or subject.strip() == "":
        return {
            "status": "error",
            "message": "Subject is required"
        }

    cur.execute("""
        INSERT INTO study_sessions (user_id, subject, chapter_name, date, minutes, focus, method, rating)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)       
    """, (user_id, subject, chapter_name, date, minutes, focus, study_method, rating))

    conn.commit()
    cur.close()
    conn.close()

    return {"status": "success"}


def get_study_sessions(user_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM study_sessions WHERE user_id = %s", (user_id, ))
    result = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {"id": r[0],
         "user_id": r[1],
         "subject": r[2],
         "chapter_name": r[3],
         "date": str(r[4]),
         "minutes": r[5],
         "focus": r[6],
         "method": r[7],
         "rating": r[8]}
        for r in result
    ]


def delete_study_session(session_id, user_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM study_sessions
        WHERE id = %s AND user_id = %s
    """, (session_id, user_id))

    conn.commit()
    cur.close()
    conn.close()

    return {"status": "deleted",
            "Rows deleted": cur.rowcount}


def update_study_session(session_id, user_id, subject, date, study_time, focus, method, rating, chapter_name):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        UPDATE study_sessions
        SET subject = %s,
            date = %s,
            minutes = %s,
            focus = %s,
            method = %s,
            rating = %s,
            chapter_name = %s
        WHERE id = %s AND user_id = %s
    """, (subject, date, study_time, focus, method, rating, chapter_name, session_id, user_id))

    conn.commit()
    cur.close()
    conn.close()

    return {"status": "updated"}
