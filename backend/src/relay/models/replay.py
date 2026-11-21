import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    LargeBinary,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from relay.db.base import Base


class ReplayAttempt(Base):
    __tablename__ = "replay_attempts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("webhook_requests.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    destination_url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    method: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    request_headers: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )

    request_body: Mapped[bytes] = mapped_column(
        LargeBinary,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    response_status_code: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    response_headers: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    response_body: Mapped[bytes | None] = mapped_column(
        LargeBinary,
        nullable=True,
    )

    duration_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    error: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
