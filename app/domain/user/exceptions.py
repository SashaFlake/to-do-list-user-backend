class UserDomainError(Exception):
    """Base domain error for user aggregate."""


class UserAlreadyExistsError(UserDomainError):
    def __init__(self, email: str) -> None:
        super().__init__(f"User with email '{email}' already exists")


class UserNotFoundError(UserDomainError):
    def __init__(self, identifier: str) -> None:
        super().__init__(f"User '{identifier}' not found")


class UserInactiveError(UserDomainError):
    def __init__(self) -> None:
        super().__init__("User account is inactive")
