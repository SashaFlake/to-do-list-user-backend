from keycloak import KeycloakAdmin, KeycloakOpenID
from keycloak.exceptions import KeycloakAuthenticationError, KeycloakPostError

from src.application.user.dto import TokenResponseDTO
from src.application.user.ports import AbstractKeycloakPort
from src.core.config import settings
from src.domain.user.exceptions import UserAlreadyExistsError


class KeycloakAdapter(AbstractKeycloakPort):
    def __init__(self) -> None:
        self._openid = KeycloakOpenID(
            server_url=settings.keycloak_server_url,
            realm_name=settings.keycloak_realm,
            client_id=settings.keycloak_client_id,
            client_secret_key=settings.keycloak_client_secret,
        )
        self._admin = KeycloakAdmin(
            server_url=settings.keycloak_server_url,
            username=settings.keycloak_admin_username,
            password=settings.keycloak_admin_password,
            realm_name=settings.keycloak_realm,
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
                raise UserAlreadyExistsError(email) from exc
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
            raise ValueError("Invalid credentials") from exc

    async def refresh_token(self, refresh_token: str) -> TokenResponseDTO:
        token = self._openid.refresh_token(refresh_token)
        return TokenResponseDTO(
            access_token=token["access_token"],
            refresh_token=token["refresh_token"],
            token_type=token["token_type"],
            expires_in=token["expires_in"],
        )

    async def delete_user(self, keycloak_id: str) -> None:
        self._admin.delete_user(keycloak_id)

    async def update_user_email(self, keycloak_id: str, new_email: str) -> None:
        self._admin.update_user(keycloak_id, {"email": new_email})
