from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.user.entity import User
from app.domain.user.repository import AbstractUserRepository
from app.domain.user.value_objects import Email, ExternalIdentityId, Username
from app.infrastructure.db.models import UserModel


class SQLAlchemyUserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_external_id(self, external_id: str) -> User | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.external_id == external_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def save(self, user: User) -> None:
        model = UserModel(
            id=user.id,
            email=str(user.email),
            username=str(user.username),
            external_id=str(user.external_id),
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        self._session.add(model)
        await self._session.commit()

    async def update(self, user: User) -> None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == user.id)
        )
        model = result.scalar_one()
        model.username = str(user.username)
        model.email = str(user.email)
        model.is_active = user.is_active
        model.updated_at = user.updated_at
        await self._session.commit()

    @staticmethod
    def _to_entity(model: UserModel) -> User:
        return User(
            id=model.id,
            email=Email(model.email),
            username=Username(model.username),
            external_id=ExternalIdentityId(model.external_id),
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
