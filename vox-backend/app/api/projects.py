from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import (
    get_current_user,
    require_roles,
)
from app.db.database import get_db
from app.models.project import Project
from app.models.user import User, UserRole
from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)


router = APIRouter()


def build_project_response(
    project: Project,
    dialogue_count: int = 0,
) -> ProjectResponse:
    project_status = (
        "ready"
        if dialogue_count >= 10
        else "insufficient_data"
    )

    return ProjectResponse(
        id=project.id,
        company_id=project.company_id,
        name=project.name,
        target_service=project.target_service,
        description=project.description,
        dialogue_count=dialogue_count,
        status=project_status,
        created_at=project.created_at,
    )


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    data: ProjectCreate,
    current_user: User = Depends(
        require_roles(
            UserRole.OWNER,
            UserRole.MARKETER,
        )
    ),
    db: AsyncSession = Depends(get_db),
):
    project = Project(
        company_id=current_user.company_id,
        name=data.name,
        target_service=data.target_service,
        description=data.description,
    )

    db.add(project)

    await db.commit()
    await db.refresh(project)

    return build_project_response(
        project=project,
        dialogue_count=0,
    )


@router.get(
    "",
    response_model=list[ProjectResponse],
)
async def get_projects(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(Project)
        .where(
            Project.company_id == current_user.company_id
        )
        .order_by(Project.created_at.desc())
    )

    result = await db.execute(query)

    projects = result.scalars().all()

    return [
        build_project_response(
            project=project,
            dialogue_count=0,
        )
        for project in projects
    ]


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
async def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(Project).where(
        Project.id == project_id,
        Project.company_id == current_user.company_id,
    )

    result = await db.execute(query)

    project = result.scalar_one_or_none()

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return build_project_response(
        project=project,
        dialogue_count=0,
    )


@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
)
async def update_project(
    project_id: int,
    data: ProjectUpdate,
    current_user: User = Depends(
        require_roles(
            UserRole.OWNER,
            UserRole.MARKETER,
        )
    ),
    db: AsyncSession = Depends(get_db),
):
    query = select(Project).where(
        Project.id == project_id,
        Project.company_id == current_user.company_id,
    )

    result = await db.execute(query)

    project = result.scalar_one_or_none()

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    update_data = data.model_dump(
        exclude_unset=True,
    )

    for field, value in update_data.items():
        setattr(
            project,
            field,
            value,
        )

    await db.commit()
    await db.refresh(project)

    return build_project_response(
        project=project,
        dialogue_count=0,
    )


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project(
    project_id: int,
    current_user: User = Depends(
        require_roles(
            UserRole.OWNER,
            UserRole.MARKETER,
        )
    ),
    db: AsyncSession = Depends(get_db),
):
    query = select(Project).where(
        Project.id == project_id,
        Project.company_id == current_user.company_id,
    )

    result = await db.execute(query)

    project = result.scalar_one_or_none()

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    await db.delete(project)
    await db.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )