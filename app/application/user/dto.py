from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

if TYPE_CHECKING:
    from app.domain.user.entity import User


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

    @classmethod
    def from_entity(cls, user: "User") -> "UserResponseDTO":
        return cls(
            id=user.id,
            email=str(user.email),
            username=str(user.username),
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


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
