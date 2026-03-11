from fastapi import APIRouter, HTTPException, status

from src.application.user.dto import LoginDTO, RefreshTokenDTO, RegisterUserDTO, TokenResponseDTO, UserResponseDTO
from src.api.dependencies import get_keycloak_adapter, get_user_repository
from src.application.user.use_cases import LoginUseCase, RefreshTokenUseCase, RegisterUserUseCase
from src.domain.user.exceptions import UserAlreadyExistsError
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.db.session import get_db_session

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=UserResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def register(
    dto: RegisterUserDTO,
    session: AsyncSession = Depends(get_db_session),
) -> UserResponseDTO:
    use_case = RegisterUserUseCase(
        user_repo=get_user_repository(session),
        keycloak=get_keycloak_adapter(),
    )
    try:
        return await use_case.execute(dto)
    except UserAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.post(
    "/login",
    response_model=TokenResponseDTO,
    summary="Login and get tokens",
)
async def login(dto: LoginDTO) -> TokenResponseDTO:
    use_case = LoginUseCase(keycloak=get_keycloak_adapter())
    try:
        return await use_case.execute(dto)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))


@router.post(
    "/refresh",
    response_model=TokenResponseDTO,
    summary="Refresh access token",
)
async def refresh(dto: RefreshTokenDTO) -> TokenResponseDTO:
    use_case = RefreshTokenUseCase(keycloak=get_keycloak_adapter())
    try:
        return await use_case.execute(dto)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
