import uuid
from fastapi import HTTPException, status
from jose import JWTError, jwt
from config.setting import JWT_SECRET_KEY
from config import JWT_SECRET_KEY

from datetime import timedelta, datetime as dt


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = dt.datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
    # Random_ID is used to generate the new token each time login
    to_encode.update({"random_id": str(uuid.uuid4())})

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY)
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You need to sign in access this page",
            headers={"WWW-Authenticate": "Bearer"},
        )
