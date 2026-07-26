from database import connect


def add_subject(user_id, name, priority):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO subjects (user_id, name, priority)
    VALUES (%s, %s, %s)     
    """, (user_id, name, priority))

    conn.commit()
    cur.close()
    conn.close()

    return {"status": "success"}


def get_subjects(user_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT * FROM subjects
    WHERE user_id = %s         
    """, (user_id, ))
    result = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {"id": r[0],
         "name": r[1],
         "priority": r[2]}
        for r in result
    ]
