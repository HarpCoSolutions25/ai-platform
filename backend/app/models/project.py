import uuid
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List


class Project(SQLModel, table=True):
    __tablename__ = "project"

    id: int = Field(primary_key=True)
    name: str = Field(max_length=255, unique=True)

    # Placeholder for relationship with users
    users: List["ProjectUser"] = Relationship(back_populates="project",cascade_delete="all, delete")
