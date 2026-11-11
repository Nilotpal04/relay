from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, model_validator

class WebhookRequestSummary(BaseModel):
    id: UUID
    method: str
    content_type: str | None
    source_ip: str | None
    received_at: datetime

    model_config = ConfigDict(from_attributes=True)

class WebhookRequestDetail(BaseModel):
    id: UUID
    endpoint_id: UUID
    method: str
    headers: dict
    query_params: dict
    content_type: str | None
    source_ip: str | None
    received_at: datetime

    body_content: str
    body_encoding: str

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    @classmethod
    def process_body(cls, V):
        pass

