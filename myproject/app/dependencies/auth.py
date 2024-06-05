from typing import Annotated
from config.setting import JWT_SECRET_KEY
from config import JWT_SECRET_KEY, spark
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from spark import spark_admin
from services import users
from exceptions import SessionException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = spark()
    try:
        yield db
    finally:
        db.close()


def authenticate_token_and_get_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: spark = Depends(get_db)
):
    credentials_exception = SessionException("Session has Expired")
    try:
        if not token:
            raise SessionException("You need to sign in to access this page")

        payload = jwt.decode(token, JWT_SECRET_KEY)
        current_user = users.get_user_by_id(payload.get("id"), db)

        if current_user.access_token != token:
            raise SessionException("Session has expired")
    except JWTError:
        raise credentials_exception
    except HTTPException as e:
        raise e
    return current_user

