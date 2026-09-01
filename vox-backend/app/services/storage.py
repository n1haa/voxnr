import asyncio
from pathlib import Path
from uuid import uuid4

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import HTTPException, UploadFile, status

from app.core.config import settings


MAX_FILE_SIZE = 100 * 1024 * 1024

ALLOWED_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".m4a",
    ".txt",
    ".json",
    ".pdf",
}


s3_client = boto3.client(
    "s3",
    endpoint_url=settings.S3_ENDPOINT_URL,
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_KEY,
    region_name=settings.S3_REGION,
    config=Config(
        signature_version="s3v4",
        s3={
            "addressing_style": settings.S3_ADDRESSING_STYLE,
        },
    ),
)


async def get_file_size(
    file: UploadFile,
) -> int:
    def calculate_size() -> int:
        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)

        return size

    return await asyncio.to_thread(
        calculate_size
    )


async def upload_file_to_storage(
    file: UploadFile,
    company_id: int,
    project_id: int,
) -> tuple[str, int]:
    original_filename = file.filename

    if not original_filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required",
        )

    extension = Path(
        original_filename
    ).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=(
                "Unsupported file type. "
                "Allowed: MP3, WAV, M4A, TXT, JSON, PDF"
            ),
        )

    file_size = await get_file_size(file)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds 100 MB",
        )

    if file_size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is empty",
        )

    storage_key = (
        f"companies/{company_id}/"
        f"projects/{project_id}/"
        f"dialogues/{uuid4()}{extension}"
    )

    content_type = (
            file.content_type
            or "application/octet-stream"
    )

    if extension in {".txt", ".json"}:
        content_type = f"{content_type}; charset=utf-8"

    extra_args = {
        "ContentType": content_type,
    }

    if settings.S3_SERVER_SIDE_ENCRYPTION:
        extra_args["ServerSideEncryption"] = (
            settings.S3_SERVER_SIDE_ENCRYPTION
        )

    await file.seek(0)

    try:
        await asyncio.to_thread(
            s3_client.upload_fileobj,
            file.file,
            settings.S3_BUCKET,
            storage_key,
            ExtraArgs=extra_args,
        )

    except (BotoCoreError, ClientError) as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to upload file to object storage",
        ) from exc

    finally:
        await file.close()

    return storage_key, file_size


async def delete_file_from_storage(
    storage_key: str,
) -> None:
    try:
        await asyncio.to_thread(
            s3_client.delete_object,
            Bucket=settings.S3_BUCKET,
            Key=storage_key,
        )

    except (BotoCoreError, ClientError):
        pass


async def generate_download_url(
    storage_key: str,
) -> str:
    try:
        return await asyncio.to_thread(
            s3_client.generate_presigned_url,
            "get_object",
            Params={
                "Bucket": settings.S3_BUCKET,
                "Key": storage_key,
            },
            ExpiresIn=(
                settings
                .S3_PRESIGNED_URL_EXPIRE_SECONDS
            ),
        )

    except (BotoCoreError, ClientError) as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to generate download URL",
        ) from exc