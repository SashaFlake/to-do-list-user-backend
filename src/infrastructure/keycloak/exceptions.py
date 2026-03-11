class KeycloakInfraError(Exception):
    """Base infrastructure error for Keycloak operations."""


class KeycloakUserAlreadyExistsError(KeycloakInfraError):
    def __init__(self, email: str) -> None:
        super().__init__(f"Keycloak: user with email '{email}' already exists")


class KeycloakAuthError(KeycloakInfraError):
    def __init__(self) -> None:
        super().__init__("Keycloak: invalid credentials")


class KeycloakTokenError(KeycloakInfraError):
    def __init__(self) -> None:
        super().__init__("Keycloak: invalid or expired token")
