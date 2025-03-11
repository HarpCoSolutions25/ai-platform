from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.schemas.project_user import ProjectUserResponse
from app.crud.project_user import (
    add_user_to_project,
    remove_user_from_project,
    get_users_by_project,
    is_admin,
    is_user_in_project,
)
from app.api.deps import get_db
from app.api.deps import get_current_user
from app.models import User, Project

router = APIRouter(prefix="/projects/{project_id}", tags=["project_user"])


@router.post("/users/{user_id}", response_model=ProjectUserResponse)
def add_user_to_project(
    project_id: int,
    user_id: UUID,
    admin: bool = False,  # Allow specifying admin role
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Add a user to a project (only if the current user is an admin or superuser)."""

    # Check if project exists
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Allow superusers to manage projects
    if not current_user.is_superuser and not is_admin(db, project_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to add users to this project."
        )

    # Ensure user is not already in the project
    if is_user_in_project(db, project_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member of this project."
        )

    new_project_user = add_user_to_project(db, project_id, user_id, admin)
    return new_project_user

@router.get("/users/", response_model=List[ProjectUserResponse])
def list_users_in_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all users related to a project, only if the requester is part of the project."""
    
    # Check if project exists before querying users
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Allow superusers to view any project
    if not current_user.is_superuser and not is_user_in_project(db, project_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view users in this project."
        )
    return get_users_by_project(db, project_id)

@router.delete("/users/{user_id}", response_model=ProjectUserResponse)
def remove_user_from_project(
    project_id: int,
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Remove a user from a project (only if the current user is an admin or superuser)."""

    # Check if project exists
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Allow superusers to remove any user from any project
    if not current_user.is_superuser and not is_admin(db, project_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to remove users from this project."
        )

    # Ensure the user is in the project before removing
    if not is_user_in_project(db, project_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User is not a member of this project."
        )

    deleted_user = remove_user_from_project(db, project_id, user_id)
    return deleted_user