import base64
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
    def process_body(cls, values):
        data = {
            "id": values.id,
            "endpoint_id": values.endpoint_id,
            "method": values.method,
            "headers": values.headers,
            "query_params": values.query_params,
            "content_type": values.content_type,
            "source_ip": values.source_ip,
            "received_at": values.received_at,
        }

        body = values.body

        try:
            data["body_content"] = body.decode("utf-8")
            data["body_encoding"] = "utf-8"

        except UnicodeDecodeError:
            data["body_content"] = base64.b64encode(body).decode("ascii")
            data["body_encoding"] = "base64"

        return data

