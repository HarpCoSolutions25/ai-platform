import uuid
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional


class ProjectUser(SQLModel, table=True):
    __tablename__ = "project_user"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    project_id: int = Field(foreign_key="project.id", nullable=False)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    is_admin: bool = Field(default=False, nullable=False)  # Determines if user is an admin of the project

    created_at: datetime = Field(default_factory=lambda: datetime.utcnow())
    updated_at: datetime = Field(default_factory=lambda: datetime.utcnow(), nullable=False)
    is_deleted: bool = Field(default=False, nullable=False)
    deleted_at: Optional[datetime] = Field(default=None, nullable=True)

    # Relationships
    project: Optional["Project"] = Relationship(back_populates="users")
    user: Optional["User"] = Relationship(back_populates="projects")
