import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    JSON,
    LargeBinary,
    String,
    func,
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from relay.db.base import Base

class WebhookRequest(Base):
    __tablename__ = "webhook_requests"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    endpoint_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("endpoints.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    method: Mapped[str] = mapped_column(
        String(10)
    )

    headers: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )

    query_params: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )

    body: Mapped[bytes] = mapped_column(
        LargeBinary,
        nullable=False,
    )

    content_type: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    source_ip: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True,
    )

    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    __table_args__ = (
        Index (
            "ix_webhook_resquests_endpoint_recieved",
            "endpoint_id",
            "received_at",
        ),
    )

