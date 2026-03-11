from abc import ABC, abstractmethod

from src.application.user.dto import TokenResponseDTO


class AbstractKeycloakPort(ABC):
    """Port for Keycloak IAM operations."""

    @abstractmethod
    async def create_user(
        self,
        email: str,
        username: str,
        password: str,
    ) -> str:
        """Create user in Keycloak, return keycloak_id."""
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
    async def delete_user(self, keycloak_id: str) -> None:
        ...

    @abstractmethod
    async def update_user_email(self, keycloak_id: str, new_email: str) -> None:
        ...
