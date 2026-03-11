from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class RegisterUserDTO(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)


class UpdateUserDTO(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=50)


class UserResponseDTO(BaseModel):
    id: UUID
    email: str
    username: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TokenResponseDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class LoginDTO(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenDTO(BaseModel):
    refresh_token: str
