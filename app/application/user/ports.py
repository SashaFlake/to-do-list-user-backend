from abc import ABC, abstractmethod

from app.application.user.dto import TokenResponseDTO


class AbstractKeycloakPort(ABC):
    """Port for Keycloak IAM operations."""

    @abstractmethod
    async def create_user(
        self,
        email: str,
        username: str,
        password: str,
    ) -> str:
        """Create user in IAM provider, return external_id."""
        ...

    @abstractmethod
    async def authenticate(
        self,
        email: str,
        password: str,
    ) -> TokenResponseDTO:
        ...

    @abstractmethod
    async def refresh_token(self, refresh_token: str) -> TokenResponseDTO:
        ...

    @abstractmethod
    async def delete_user(self, external_id: str) -> None:
        ...

    @abstractmethod
    async def update_user_email(self, external_id: str, new_email: str) -> None:
        ...
