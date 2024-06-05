from pydantic import BaseModel, EmailStr


class SignInParams(BaseModel):
    email: EmailStr
    password: str