from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from src.domain.user.value_objects import Email, ExternalIdentityId, Username


@dataclass
class User:
    id: UUID
    email: Email
    username: Username
    external_id: ExternalIdentityId  # IAM provider ID (opaque to domain)
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        email: str,
        username: str,
        external_id: str,
    ) -> "User":
        now = datetime.utcnow()
        return cls(
            id=uuid4(),
            email=Email(email),
            username=Username(username),
            external_id=ExternalIdentityId(external_id),
            is_active=True,
            created_at=now,
            updated_at=now,
        )

    def deactivate(self) -> None:
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def update_username(self, username: str) -> None:
        self.username = Username(username)
        self.updated_at = datetime.utcnow()
