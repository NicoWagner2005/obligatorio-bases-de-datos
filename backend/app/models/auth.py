from pydantic import BaseModel, EmailStr

class RegistrationCredentials(BaseModel):
    ci: str
    name: str
    surname: str
    email: EmailStr
    password: str

class RegistrationResponse(BaseModel):
    message: str

class LoginCredentials(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    message: str
    user_id: int
    ci: str
    token: str
    admin: bool
