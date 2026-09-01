import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    DateTime,
    Enum,
    ForeignKey,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.user import User


class DialogueLeadType(str, enum.Enum):
    HOT = "hot"
    COLD = "cold"


class DialogueStatus(str, enum.Enum):
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"


class Dialogue(Base):
    __tablename__ = "dialogues"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey(
            "projects.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    uploaded_by: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    storage_key: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        unique=True,
    )

    content_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    lead_type: Mapped[DialogueLeadType] = mapped_column(
        Enum(DialogueLeadType),
        nullable=False,
    )

    client_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    product: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[DialogueStatus] = mapped_column(
        Enum(DialogueStatus),
        nullable=False,
        default=DialogueStatus.PROCESSING,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    project: Mapped["Project"] = relationship(
        back_populates="dialogues",
    )

    uploader: Mapped["User"] = relationship(
        back_populates="dialogues",
    )