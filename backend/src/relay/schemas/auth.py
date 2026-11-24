from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    email: EmailStr
    name: str
    username: str
    password: str = Field(
        min_length=8,
        max_length=72,
        description="Password must be between 8 and 72 characters",
    )

class LoginRequest(BaseModel):
    identifier: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    is_active: bool

class AuthResponse(BaseModel):
    user: UserResponse
    tokens: TokenResponse
