from unittest.mock import AsyncMock
from uuid import uuid4
import pytest

from src.application.user.dto import RegisterUserDTO
from src.application.user.use_cases import RegisterUserUseCase
from src.domain.user.exceptions import UserAlreadyExistsError


@pytest.mark.asyncio
async def test_register_user_success() -> None:
    repo = AsyncMock()
    repo.get_by_email.return_value = None
    keycloak = AsyncMock()
    keycloak.create_user.return_value = str(uuid4())

    use_case = RegisterUserUseCase(user_repo=repo, keycloak=keycloak)
    dto = RegisterUserDTO(email="user@example.com", username="newuser", password="secret123")
    result = await use_case.execute(dto)

    assert result.email == "user@example.com"
    repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_register_user_duplicate_raises() -> None:
    repo = AsyncMock()
    repo.get_by_email.return_value = object()  # simulate existing user
    keycloak = AsyncMock()

    use_case = RegisterUserUseCase(user_repo=repo, keycloak=keycloak)
    dto = RegisterUserDTO(email="user@example.com", username="newuser", password="secret123")

    with pytest.raises(UserAlreadyExistsError):
        await use_case.execute(dto)
