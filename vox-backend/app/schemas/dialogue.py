from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DialogueResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    project_id: int
    uploaded_by: int
    original_filename: str
    content_type: str
    file_size: int
    lead_type: str
    client_name: str
    product: str
    summary: str | None
    status: str
    error_message: str | None
    created_at: datetime


class DialogueDownloadUrlResponse(BaseModel):
    url: str
    expires_in: int