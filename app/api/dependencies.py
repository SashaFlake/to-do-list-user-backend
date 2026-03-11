from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.user.ports import AbstractKeycloakPort
from app.application.user.use_cases import (
    GetUserUseCase,
    LoginUseCase,
    RefreshTokenUseCase,
    RegisterUserUseCase,
    UpdateUserUseCase,
)
from app.core.config import settings
from app.domain.user.repository import AbstractUserRepository
from app.infrastructure.db.session import get_db_session
from app.infrastructure.db.user_repository import SQLAlchemyUserRepository
from app.infrastructure.keycloak.adapter import KeycloakAdapter, KeycloakSettings


def _keycloak_settings() -> KeycloakSettings:
    return KeycloakSettings(
        server_url=settings.keycloak_server_url,
        realm=settings.keycloak_realm,
        client_id=settings.keycloak_client_id,
        client_secret=settings.keycloak_client_secret,
        admin_username=settings.keycloak_admin_username,
        admin_password=settings.keycloak_admin_password,
    )


def get_keycloak_adapter(
    config: KeycloakSettings = Depends(_keycloak_settings),
) -> AbstractKeycloakPort:
    return KeycloakAdapter(config)


def get_user_repository(
    session: AsyncSession = Depends(get_db_session),
) -> AbstractUserRepository:
    return SQLAlchemyUserRepository(session)


def get_register_use_case(
    repo: AbstractUserRepository = Depends(get_user_repository),
    keycloak: AbstractKeycloakPort = Depends(get_keycloak_adapter),
) -> RegisterUserUseCase:
    return RegisterUserUseCase(user_repo=repo, keycloak=keycloak)


def get_login_use_case(
    keycloak: AbstractKeycloakPort = Depends(get_keycloak_adapter),
) -> LoginUseCase:
    return LoginUseCase(keycloak=keycloak)


def get_refresh_use_case(
    keycloak: AbstractKeycloakPort = Depends(get_keycloak_adapter),
) -> RefreshTokenUseCase:
    return RefreshTokenUseCase(keycloak=keycloak)


def get_get_user_use_case(
    repo: AbstractUserRepository = Depends(get_user_repository),
) -> GetUserUseCase:
    return GetUserUseCase(user_repo=repo)


def get_update_use_case(
    repo: AbstractUserRepository = Depends(get_user_repository),
) -> UpdateUserUseCase:
    return UpdateUserUseCase(user_repo=repo)
