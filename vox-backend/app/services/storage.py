from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status


UPLOAD_DIR = Path("uploads")

MAX_FILE_SIZE = 100 * 1024 * 1024

ALLOWED_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".m4a",
    ".txt",
    ".json",
    ".pdf",
}


async def save_upload_file(
    file: UploadFile,
) -> tuple[str, int]:
    original_filename = file.filename

    if not original_filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required",
        )

    extension = Path(original_filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=(
                "Unsupported file type. "
                "Allowed: MP3, WAV, M4A, TXT, JSON, PDF"
            ),
        )

    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    storage_key = f"{uuid4()}{extension}"

    destination = UPLOAD_DIR / storage_key

    total_size = 0

    try:
        with destination.open("wb") as output_file:
            while chunk := await file.read(1024 * 1024):
                total_size += len(chunk)

                if total_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail="File size exceeds 100 MB",
                    )

                output_file.write(chunk)

    except Exception:
        if destination.exists():
            destination.unlink()

        raise

    finally:
        await file.close()

    return storage_key, total_size