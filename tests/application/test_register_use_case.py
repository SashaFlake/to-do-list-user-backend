from unittest.mock import AsyncMock
from uuid import uuid4
import pytest

from app.application.user.dto import RegisterUserDTO
from app.application.user.use_cases import RegisterUserUseCase
from app.domain.user.exceptions import UserAlreadyExistsError
from app.infrastructure.keycloak.exceptions import KeycloakUserAlreadyExistsError


async def test_register_user_success() -> None:
    repo = AsyncMock()
    repo.get_by_email.return_value = None
    keycloak = AsyncMock()
    keycloak.create_user.return_value = str(uuid4())

    use_case = RegisterUserUseCase(user_repo=repo, keycloak=keycloak)
    dto = RegisterUserDTO(email="user@example.com", username="newuser", password="secret123")
    result = await use_case.execute(dto)

    assert result.email == "user@example.com"
    assert result.username == "newuser"
    assert result.is_active is True
    keycloak.create_user.assert_called_once_with(
        email="user@example.com",
        username="newuser",
        password="secret123",
    )
    repo.save.assert_called_once()


async def test_register_user_duplicate_raises() -> None:
    repo = AsyncMock()
    repo.get_by_email.return_value = object()
    keycloak = AsyncMock()

    use_case = RegisterUserUseCase(user_repo=repo, keycloak=keycloak)
    dto = RegisterUserDTO(email="user@example.com", username="newuser", password="secret123")

    with pytest.raises(UserAlreadyExistsError):
        await use_case.execute(dto)


async def test_register_user_keycloak_duplicate_raises() -> None:
    repo = AsyncMock()
    repo.get_by_email.return_value = None
    keycloak = AsyncMock()
    keycloak.create_user.side_effect = KeycloakUserAlreadyExistsError()

    use_case = RegisterUserUseCase(user_repo=repo, keycloak=keycloak)
    dto = RegisterUserDTO(email="user@example.com", username="newuser", password="secret123")

    with pytest.raises(UserAlreadyExistsError):
        await use_case.execute(dto)
