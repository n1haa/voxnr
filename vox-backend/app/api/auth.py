from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.db.database import get_db
from app.models.company import Company
from app.models.user import User, UserRole
from app.schemas.auth import (
    RefreshTokenRequest,
    RegisterCompanyRequest,
    RegisterCompanyResponse,
    TokenResponse,
    UserMeResponse,
)


router = APIRouter()


@router.post(
    "/register-company",
    response_model=RegisterCompanyResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_company(
    data: RegisterCompanyRequest,
    db: AsyncSession = Depends(get_db),
):
    company_query = select(Company).where(
        Company.inn == data.inn
    )

    company_result = await db.execute(company_query)

    existing_company = company_result.scalar_one_or_none()

    if existing_company is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Company with this INN already exists",
        )

    user_query = select(User).where(
        User.email == data.email
    )

    user_result = await db.execute(user_query)

    existing_user = user_result.scalar_one_or_none()

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    company = Company(
        name=data.company_name,
        inn=data.inn,
    )

    db.add(company)

    await db.flush()

    user = User(
        company_id=company.id,
        full_name=data.full_name,
        email=data.email,
        password_hash=hash_password(data.password),
        role=UserRole.OWNER,
    )

    db.add(user)

    await db.commit()

    await db.refresh(company)
    await db.refresh(user)

    return RegisterCompanyResponse(
        company_id=company.id,
        user_id=user.id,
        email=user.email,
        role=user.role.value,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user_query = select(User).where(
        User.email == form_data.username
    )

    user_result = await db.execute(user_query)

    user = user_result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    if not verify_password(
        form_data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    access_token = create_access_token(
        user_id=user.id,
        company_id=user.company_id,
        role=user.role.value,
    )

    refresh_token = create_refresh_token(
        user_id=user.id,
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


@router.post(
    "/refresh",
    response_model=TokenResponse,
)
async def refresh_tokens(
    data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        payload = decode_token(data.refresh_token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    try:
        user_id = int(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    user = await db.get(
        User,
        user_id,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    access_token = create_access_token(
        user_id=user.id,
        company_id=user.company_id,
        role=user.role.value,
    )

    refresh_token = create_refresh_token(
        user_id=user.id,
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


@router.get(
    "/me",
    response_model=UserMeResponse,
)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    return UserMeResponse(
        id=current_user.id,
        company_id=current_user.company_id,
        full_name=current_user.full_name,
        email=current_user.email,
        role=current_user.role.value,
    )