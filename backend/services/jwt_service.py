from jose import jwt, JWTError
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone

SECRET_KEY = "arvora-secret-key-AXJTWSD429"  # placeholder for now
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Half an hour


def create_access_token(user_id, role):
    expire = datetime.now(timezone.utc) + \
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "user_id": user_id,
        "role": role,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def verify_access_token(token):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token expired or invalid"
        )

    return payload
