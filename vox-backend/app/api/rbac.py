from fastapi import APIRouter, Depends

from app.api.dependencies import require_roles
from app.models.user import User, UserRole


router = APIRouter()


@router.get("/owner-only")
async def owner_only(
    current_user: User = Depends(
        require_roles(
            UserRole.OWNER,
        )
    ),
):
    return {
        "message": "Owner access granted",
        "user_id": current_user.id,
        "role": current_user.role.value,
    }


@router.get("/management")
async def management_only(
    current_user: User = Depends(
        require_roles(
            UserRole.OWNER,
            UserRole.MARKETER,
        )
    ),
):
    return {
        "message": "Management access granted",
        "user_id": current_user.id,
        "role": current_user.role.value,
    }