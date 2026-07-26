from database import connect
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from .jwt_service import create_access_token

ph = PasswordHasher()


def register_user(username, password):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM users WHERE username = %s",
        (username,)
    )

    existing_user = cur.fetchone()

    if existing_user:
        cur.close()
        conn.close()
        return {
            "status": "error",
            "message": "Username already exists"
        }

    password_hash = ph.hash(password)

    cur.execute("""
        INSERT INTO users (username, password_hash, role)
        VALUES (%s, %s, %s)
    """, (username, password_hash, "student"))

    conn.commit()

    cur.close()
    conn.close()

    return {
        "status": "success"
    }


def login_user(username, password):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, username, password_hash
        FROM users
        WHERE username = %s
    """, (username,))

    user = cur.fetchone()

    cur.close()
    conn.close()

    if not user:
        return {
            "status": "error",
            "message": "Invalid username or password"
        }

    try:
        ph.verify(user[2], password)

        token = create_access_token(user[0], "student")

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    except VerifyMismatchError:
        return {
            "status": "error",
            "message": "Invalid username or password"
        }
