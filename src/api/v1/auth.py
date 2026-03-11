from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies import (
    get_login_use_case,
    get_refresh_use_case,
    get_register_use_case,
)
from src.application.user.dto import (
    LoginDTO,
    RefreshTokenDTO,
    RegisterUserDTO,
    TokenResponseDTO,
    UserResponseDTO,
)
from src.application.user.use_cases import (
    LoginUseCase,
    RefreshTokenUseCase,
    RegisterUserUseCase,
)
from src.domain.user.exceptions import UserAlreadyExistsError

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=UserResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def register(
    dto: RegisterUserDTO,
    use_case: RegisterUserUseCase = Depends(get_register_use_case),
) -> UserResponseDTO:
    try:
        return await use_case.execute(dto)
    except UserAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.post(
    "/login",
    response_model=TokenResponseDTO,
    summary="Login and get tokens",
)
async def login(
    dto: LoginDTO,
    use_case: LoginUseCase = Depends(get_login_use_case),
) -> TokenResponseDTO:
    try:
        return await use_case.execute(dto)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))


@router.post(
    "/refresh",
    response_model=TokenResponseDTO,
    summary="Refresh access token",
)
async def refresh(
    dto: RefreshTokenDTO,
    use_case: RefreshTokenUseCase = Depends(get_refresh_use_case),
) -> TokenResponseDTO:
    try:
        return await use_case.execute(dto)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))
