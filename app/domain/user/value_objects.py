import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        pattern = r'^[\w.+-]+@[\w-]+\.[\w.]+$'
        if not re.match(pattern, self.value):
            raise ValueError(f"Invalid email: {self.value}")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Username:
    value: str

    def __post_init__(self) -> None:
        if len(self.value) < 3 or len(self.value) > 50:
            raise ValueError("Username must be between 3 and 50 characters")
        if not re.match(r'^[\w.-]+$', self.value):
            raise ValueError("Username contains invalid characters")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class ExternalIdentityId:
    """Opaque external IAM provider identifier (e.g. Keycloak user ID)."""

    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("ExternalIdentityId cannot be empty")

    def __str__(self) -> str:
        return self.value
