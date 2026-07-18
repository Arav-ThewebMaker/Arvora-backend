from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from .jwt_service import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_access_token(token)
        return {
            "user_id": payload["user_id"],
            "role": payload["role"]
        }
    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
