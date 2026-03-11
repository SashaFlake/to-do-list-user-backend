import pytest
from app.domain.user.entity import User
from app.domain.user.value_objects import Email, ExternalIdentityId, Username


def test_create_user() -> None:
    user = User.create(
        email="test@example.com",
        username="testuser",
        external_id="kc-123",
    )
    assert str(user.email) == "test@example.com"
    assert str(user.username) == "testuser"
    assert user.is_active is True


def test_deactivate_user() -> None:
    user = User.create("test@example.com", "testuser", "kc-123")
    old_updated_at = user.updated_at
    user.deactivate()
    assert user.is_active is False
    assert user.updated_at >= old_updated_at


def test_update_username() -> None:
    user = User.create("test@example.com", "testuser", "kc-123")
    old_updated_at = user.updated_at
    user.update_username("newname")
    assert str(user.username) == "newname"
    assert user.updated_at >= old_updated_at


def test_invalid_email_raises() -> None:
    with pytest.raises(ValueError):
        Email("not-an-email")


def test_short_username_raises() -> None:
    with pytest.raises(ValueError):
        Username("ab")


def test_invalid_username_chars_raises() -> None:
    with pytest.raises(ValueError):
        Username("user name!")


def test_empty_external_id_raises() -> None:
    with pytest.raises(ValueError):
        ExternalIdentityId("")
