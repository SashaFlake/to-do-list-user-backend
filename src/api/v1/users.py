from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import get_user_repository
from src.application.user.dto import UpdateUserDTO, UserResponseDTO
from src.application.user.use_cases import GetUserUseCase, UpdateUserUseCase
from src.domain.user.exceptions import UserNotFoundError
from src.infrastructure.db.session import get_db_session

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/{user_id}",
    response_model=UserResponseDTO,
    summary="Get user by ID",
)
async def get_user(
    user_id: UUID,
    session: AsyncSession = Depends(get_db_session),
) -> UserResponseDTO:
    use_case = GetUserUseCase(user_repo=get_user_repository(session))
    try:
        return await use_case.execute(user_id)
    except UserNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.patch(
    "/{user_id}",
    response_model=UserResponseDTO,
    summary="Update user profile",
)
async def update_user(
    user_id: UUID,
    dto: UpdateUserDTO,
    session: AsyncSession = Depends(get_db_session),
) -> UserResponseDTO:
    use_case = UpdateUserUseCase(user_repo=get_user_repository(session))
    try:
        return await use_case.execute(user_id, dto)
    except UserNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
