from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_get_user_use_case, get_update_use_case
from app.application.user.dto import UpdateUserDTO, UserResponseDTO
from app.application.user.use_cases import GetUserUseCase, UpdateUserUseCase
from app.domain.user.exceptions import UserNotFoundError

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/{user_id}",
    response_model=UserResponseDTO,
    summary="Get user by ID",
)
async def get_user(
    user_id: UUID,
    use_case: GetUserUseCase = Depends(get_get_user_use_case),
) -> UserResponseDTO:
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
    use_case: UpdateUserUseCase = Depends(get_update_use_case),
) -> UserResponseDTO:
    try:
        return await use_case.execute(user_id, dto)
    except UserNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
