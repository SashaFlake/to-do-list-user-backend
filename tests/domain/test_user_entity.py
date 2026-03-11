import pytest
from src.domain.user.entity import User
from src.domain.user.value_objects import Email, Username


def test_create_user() -> None:
    user = User.create(
        email="test@example.com",
        username="testuser",
        keycloak_id="kc-123",
    )
    assert str(user.email) == "test@example.com"
    assert str(user.username) == "testuser"
    assert user.is_active is True


def test_deactivate_user() -> None:
    user = User.create("test@example.com", "testuser", "kc-123")
    user.deactivate()
    assert user.is_active is False


def test_invalid_email_raises() -> None:
    with pytest.raises(ValueError):
        Email("not-an-email")


def test_short_username_raises() -> None:
    with pytest.raises(ValueError):
        Username("ab")
