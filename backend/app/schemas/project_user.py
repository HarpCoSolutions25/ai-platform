from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ProjectUserBase(BaseModel):
    project_id: int
    user_id: UUID


class ProjectUserCreate(ProjectUserBase):
    pass


class ProjectUserResponse(ProjectUserBase):
    id: UUID
    is_admin: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
