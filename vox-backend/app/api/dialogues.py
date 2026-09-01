from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import (
    get_current_user,
    require_roles,
)
from app.core.config import settings
from app.db.database import get_db
from app.models.dialogue import (
    Dialogue,
    DialogueLeadType,
    DialogueStatus,
)
from app.models.project import Project
from app.models.user import User, UserRole
from app.schemas.dialogue import (
    DialogueDownloadUrlResponse,
    DialogueResponse,
)
from app.services.storage import (
    delete_file_from_storage,
    generate_download_url,
    upload_file_to_storage,
)
from app.tasks.dialogue_tasks import process_dialogue


router = APIRouter()


def build_dialogue_response(
    dialogue: Dialogue,
) -> DialogueResponse:
    return DialogueResponse(
        id=dialogue.id,
        project_id=dialogue.project_id,
        uploaded_by=dialogue.uploaded_by,
        original_filename=dialogue.original_filename,
        content_type=dialogue.content_type,
        file_size=dialogue.file_size,
        lead_type=dialogue.lead_type.value,
        client_name=dialogue.client_name,
        product=dialogue.product,
        summary=dialogue.summary,
        status=dialogue.status.value,
        error_message=dialogue.error_message,
        created_at=dialogue.created_at,
    )


async def get_project_for_company(
    project_id: int,
    company_id: int,
    db: AsyncSession,
) -> Project:
    query = select(Project).where(
        Project.id == project_id,
        Project.company_id == company_id,
    )

    result = await db.execute(query)

    project = result.scalar_one_or_none()

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return project


async def get_dialogue_for_user(
    dialogue_id: int,
    current_user: User,
    db: AsyncSession,
) -> Dialogue:
    if current_user.role == UserRole.CREATOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view dialogues",
        )

    query = (
        select(Dialogue)
        .join(Project)
        .where(
            Dialogue.id == dialogue_id,
            Project.company_id == current_user.company_id,
        )
    )

    if current_user.role == UserRole.SALES:
        query = query.where(
            Dialogue.uploaded_by == current_user.id
        )

    result = await db.execute(query)

    dialogue = result.scalar_one_or_none()

    if dialogue is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dialogue not found",
        )

    return dialogue


@router.post(
    "/projects/{project_id}/dialogues",
    response_model=DialogueResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_dialogue(
    project_id: int,
    lead_type: DialogueLeadType = Form(...),
    client_name: str = Form(...),
    product: str = Form(...),
    summary: str | None = Form(default=None),
    file: UploadFile = File(...),
    current_user: User = Depends(
        require_roles(
            UserRole.OWNER,
            UserRole.MARKETER,
            UserRole.SALES,
        )
    ),
    db: AsyncSession = Depends(get_db),
):
    await get_project_for_company(
        project_id=project_id,
        company_id=current_user.company_id,
        db=db,
    )

    original_filename = (
        file.filename or "unknown"
    )

    content_type = (
        file.content_type
        or "application/octet-stream"
    )

    storage_key, file_size = (
        await upload_file_to_storage(
            file=file,
            company_id=current_user.company_id,
            project_id=project_id,
        )
    )

    dialogue = Dialogue(
        project_id=project_id,
        uploaded_by=current_user.id,
        original_filename=original_filename,
        storage_key=storage_key,
        content_type=content_type,
        file_size=file_size,
        lead_type=lead_type,
        client_name=client_name,
        product=product,
        summary=summary,
        status=DialogueStatus.PROCESSING,
    )

    db.add(dialogue)

    try:
        await db.commit()
        await db.refresh(dialogue)

    except Exception:
        await db.rollback()

        await delete_file_from_storage(
            storage_key
        )

        raise

    try:
        process_dialogue.delay(
            dialogue.id
        )

    except Exception as exc:
        dialogue.status = DialogueStatus.ERROR
        dialogue.error_message = (
            "Failed to enqueue dialogue processing"
        )

        await db.commit()
        await db.refresh(dialogue)

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Processing queue is unavailable",
        ) from exc

    return build_dialogue_response(
        dialogue
    )


@router.get(
    "/projects/{project_id}/dialogues",
    response_model=list[DialogueResponse],
)
async def get_project_dialogues(
    project_id: int,
    current_user: User = Depends(
        get_current_user
    ),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role == UserRole.CREATOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view dialogues",
        )

    await get_project_for_company(
        project_id=project_id,
        company_id=current_user.company_id,
        db=db,
    )

    query = (
        select(Dialogue)
        .where(
            Dialogue.project_id == project_id,
        )
        .order_by(
            Dialogue.created_at.desc()
        )
    )

    if current_user.role == UserRole.SALES:
        query = query.where(
            Dialogue.uploaded_by == current_user.id
        )

    result = await db.execute(query)

    dialogues = result.scalars().all()

    return [
        build_dialogue_response(dialogue)
        for dialogue in dialogues
    ]


@router.get(
    "/dialogues/{dialogue_id}",
    response_model=DialogueResponse,
)
async def get_dialogue(
    dialogue_id: int,
    current_user: User = Depends(
        get_current_user
    ),
    db: AsyncSession = Depends(get_db),
):
    dialogue = await get_dialogue_for_user(
        dialogue_id=dialogue_id,
        current_user=current_user,
        db=db,
    )

    return build_dialogue_response(
        dialogue
    )


@router.get(
    "/dialogues/{dialogue_id}/download-url",
    response_model=DialogueDownloadUrlResponse,
)
async def get_dialogue_download_url(
    dialogue_id: int,
    current_user: User = Depends(
        get_current_user
    ),
    db: AsyncSession = Depends(get_db),
):
    dialogue = await get_dialogue_for_user(
        dialogue_id=dialogue_id,
        current_user=current_user,
        db=db,
    )

    url = await generate_download_url(
        dialogue.storage_key
    )

    return DialogueDownloadUrlResponse(
        url=url,
        expires_in=(
            settings
            .S3_PRESIGNED_URL_EXPIRE_SECONDS
        ),
    )