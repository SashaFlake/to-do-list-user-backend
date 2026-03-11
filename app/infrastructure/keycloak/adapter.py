from keycloak import KeycloakAdmin, KeycloakOpenID
from keycloak.exceptions import KeycloakAuthenticationError, KeycloakPostError

from app.application.user.dto import TokenResponseDTO
from app.application.user.ports import AbstractKeycloakPort
from app.infrastructure.keycloak.exceptions import (
    KeycloakAuthError,
    KeycloakTokenError,
    KeycloakUserAlreadyExistsError,
)


class KeycloakSettings:
    def __init__(
        self,
        server_url: str,
        realm: str,
        client_id: str,
        client_secret: str,
        admin_username: str,
        admin_password: str,
    ) -> None:
        self.server_url = server_url
        self.realm = realm
        self.client_id = client_id
        self.client_secret = client_secret
        self.admin_username = admin_username
        self.admin_password = admin_password


class KeycloakAdapter(AbstractKeycloakPort):
    def __init__(self, config: KeycloakSettings) -> None:
        self._openid = KeycloakOpenID(
            server_url=config.server_url,
            realm_name=config.realm,
            client_id=config.client_id,
            client_secret_key=config.client_secret,
        )
        self._admin = KeycloakAdmin(
            server_url=config.server_url,
            username=config.admin_username,
            password=config.admin_password,
            realm_name=config.realm,
            verify=True,
        )

    async def create_user(
        self,
        email: str,
        username: str,
        password: str,
    ) -> str:
        try:
            keycloak_id: str = self._admin.create_user({
                "email": email,
                "username": username,
                "enabled": True,
                "credentials": [
                    {"type": "password", "value": password, "temporary": False}
                ],
            })
            return keycloak_id
        except KeycloakPostError as exc:
            if "User exists" in str(exc):
                raise KeycloakUserAlreadyExistsError(email) from exc
            raise

    async def authenticate(self, email: str, password: str) -> TokenResponseDTO:
        try:
            token = self._openid.token(email, password)
            return TokenResponseDTO(
                access_token=token["access_token"],
                refresh_token=token["refresh_token"],
                token_type=token["token_type"],
                expires_in=token["expires_in"],
            )
        except KeycloakAuthenticationError as exc:
            raise KeycloakAuthError() from exc

    async def refresh_token(self, refresh_token: str) -> TokenResponseDTO:
        try:
            token = self._openid.refresh_token(refresh_token)
            return TokenResponseDTO(
                access_token=token["access_token"],
                refresh_token=token["refresh_token"],
                token_type=token["token_type"],
                expires_in=token["expires_in"],
            )
        except Exception as exc:
            raise KeycloakTokenError() from exc

    async def delete_user(self, external_id: str) -> None:
        self._admin.delete_user(external_id)

    async def update_user_email(self, external_id: str, new_email: str) -> None:
        self._admin.update_user(external_id, {"email": new_email})
