from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class GoogleUser(BaseModel):
    sub: str
    email: str
    name: str
    picture: str
