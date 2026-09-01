from pydantic import BaseModel, EmailStr, Field


class RegisterCompanyRequest(BaseModel):
    company_name: str = Field(
        min_length=2,
        max_length=255,
    )

    inn: str = Field(
        min_length=10,
        max_length=12,
    )

    full_name: str = Field(
        min_length=2,
        max_length=255,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )


class RegisterCompanyResponse(BaseModel):
    company_id: int
    user_id: int
    email: EmailStr
    role: str