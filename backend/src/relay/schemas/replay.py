from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, HttpUrl


class ReplayCreate(BaseModel):
    destination_url: HttpUrl


class ReplayAttemptResponse(BaseModel):
    id: UUID
    request_id: UUID
    destination_url: str
    method: str
    status: str
    response_status_code: int | None
    duration_ms: int | None
    error: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
