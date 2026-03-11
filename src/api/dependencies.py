from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.user_repository import SQLAlchemyUserRepository
from src.infrastructure.keycloak.adapter import KeycloakAdapter


def get_user_repository(session: AsyncSession) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(session)


def get_keycloak_adapter() -> KeycloakAdapter:
    return KeycloakAdapter()
