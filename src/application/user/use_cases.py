from uuid import UUID

from src.application.user.dto import (
    LoginDTO,
    RefreshTokenDTO,
    RegisterUserDTO,
    TokenResponseDTO,
    UpdateUserDTO,
    UserResponseDTO,
)
from src.application.user.ports import AbstractKeycloakPort
from src.domain.user.entity import User
from src.domain.user.exceptions import UserAlreadyExistsError, UserNotFoundError
from src.domain.user.repository import AbstractUserRepository


class RegisterUserUseCase:
    def __init__(
        self,
        user_repo: AbstractUserRepository,
        keycloak: AbstractKeycloakPort,
    ) -> None:
        self._user_repo = user_repo
        self._keycloak = keycloak

    async def execute(self, dto: RegisterUserDTO) -> UserResponseDTO:
        existing = await self._user_repo.get_by_email(dto.email)
        if existing:
            raise UserAlreadyExistsError(dto.email)

        keycloak_id = await self._keycloak.create_user(
            email=dto.email,
            username=dto.username,
            password=dto.password,
        )

        user = User.create(
            email=dto.email,
            username=dto.username,
            keycloak_id=keycloak_id,
        )
        await self._user_repo.save(user)

        return UserResponseDTO(
            id=user.id,
            email=str(user.email),
            username=str(user.username),
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


class LoginUseCase:
    def __init__(self, keycloak: AbstractKeycloakPort) -> None:
        self._keycloak = keycloak

    async def execute(self, dto: LoginDTO) -> TokenResponseDTO:
        return await self._keycloak.authenticate(dto.email, dto.password)


class RefreshTokenUseCase:
    def __init__(self, keycloak: AbstractKeycloakPort) -> None:
        self._keycloak = keycloak

    async def execute(self, dto: RefreshTokenDTO) -> TokenResponseDTO:
        return await self._keycloak.refresh_token(dto.refresh_token)


class GetUserUseCase:
    def __init__(self, user_repo: AbstractUserRepository) -> None:
        self._user_repo = user_repo

    async def execute(self, user_id: UUID) -> UserResponseDTO:
        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(str(user_id))
        return UserResponseDTO(
            id=user.id,
            email=str(user.email),
            username=str(user.username),
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


class UpdateUserUseCase:
    def __init__(self, user_repo: AbstractUserRepository) -> None:
        self._user_repo = user_repo

    async def execute(self, user_id: UUID, dto: UpdateUserDTO) -> UserResponseDTO:
        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(str(user_id))

        if dto.username is not None:
            user.update_username(dto.username)

        await self._user_repo.update(user)

        return UserResponseDTO(
            id=user.id,
            email=str(user.email),
            username=str(user.username),
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
