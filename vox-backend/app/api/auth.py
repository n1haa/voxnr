from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.db.database import get_db
from app.models.company import Company
from app.models.user import User, UserRole
from app.schemas.auth import (
    RegisterCompanyRequest,
    RegisterCompanyResponse,
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