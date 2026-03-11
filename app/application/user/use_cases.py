from uuid import UUID

from app.application.user.dto import (
    LoginDTO,
    RefreshTokenDTO,
    RegisterUserDTO,
    TokenResponseDTO,
    UpdateUserDTO,
    UserResponseDTO,
)
from app.application.user.ports import AbstractKeycloakPort
from app.domain.user.entity import User
from app.domain.user.exceptions import UserAlreadyExistsError, UserNotFoundError
from app.domain.user.repository import AbstractUserRepository
from app.infrastructure.keycloak.exceptions import (
    KeycloakAuthError,
    KeycloakTokenError,
    KeycloakUserAlreadyExistsError,
)


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

        try:
            external_id = await self._keycloak.create_user(
                email=dto.email,
                username=dto.username,
                password=dto.password,
            )
        except KeycloakUserAlreadyExistsError:
            raise UserAlreadyExistsError(dto.email)

        user = User.create(
            email=dto.email,
            username=dto.username,
            external_id=external_id,
        )
        await self._user_repo.save(user)
        return UserResponseDTO.from_entity(user)


class LoginUseCase:
    def __init__(self, keycloak: AbstractKeycloakPort) -> None:
        self._keycloak = keycloak

    async def execute(self, dto: LoginDTO) -> TokenResponseDTO:
        try:
            return await self._keycloak.authenticate(dto.email, dto.password)
        except KeycloakAuthError as exc:
            raise ValueError("Invalid credentials") from exc


class RefreshTokenUseCase:
    def __init__(self, keycloak: AbstractKeycloakPort) -> None:
        self._keycloak = keycloak

    async def execute(self, dto: RefreshTokenDTO) -> TokenResponseDTO:
        try:
            return await self._keycloak.refresh_token(dto.refresh_token)
        except KeycloakTokenError as exc:
            raise ValueError("Invalid or expired refresh token") from exc


class GetUserUseCase:
    def __init__(self, user_repo: AbstractUserRepository) -> None:
        self._user_repo = user_repo

    async def execute(self, user_id: UUID) -> UserResponseDTO:
        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(str(user_id))
        return UserResponseDTO.from_entity(user)


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
        return UserResponseDTO.from_entity(user)
