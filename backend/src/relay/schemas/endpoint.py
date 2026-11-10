from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

class EndpointCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class EndpointResponse(BaseModel):
    id: UUID
    name: str
    token: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
