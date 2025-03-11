from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from datetime import datetime
from app.models.project_user import ProjectUser


def is_admin(db: Session, project_id: int, user_id: UUID) -> bool:
    """Checks if a user is an admin of the project."""
    project_user = db.query(ProjectUser).filter_by(
        project_id=project_id, user_id=user_id, is_deleted=False
    ).first()
    return project_user and project_user.is_admin


def is_user_in_project(db: Session, project_id: int, user_id: UUID) -> bool:
    """Checks if a user is already in the project."""
    return db.query(ProjectUser).filter_by(project_id=project_id, user_id=user_id, is_deleted=False).first() is not None


def add_user_to_project(db: Session, project_id: int, user_id: UUID, is_admin: bool = False):
    """Adds a user to a project with admin flag support."""
    db_project_user = ProjectUser(
        project_id=project_id,
        user_id=user_id,
        is_admin=is_admin,  # Use the passed admin flag
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(db_project_user)
    db.commit()
    db.refresh(db_project_user)
    return db_project_user


def remove_user_from_project(db: Session, project_id: int, user_id: UUID):
    """Soft deletes a user from a project."""
    project_user = db.query(ProjectUser).filter_by(project_id=project_id, user_id=user_id, is_deleted=False).first()
    if project_user:
        project_user.is_deleted = True
        project_user.deleted_at = datetime.utcnow()
        db.commit()
        return project_user
    return None


def get_users_by_project(db: Session, project_id: int):
    """Retrieves all users associated with a project."""
    return db.query(ProjectUser).filter_by(project_id=project_id, is_deleted=False).all()


def get_projects_by_user(db: Session, user_id: UUID):
    """Retrieves all projects associated with a user."""
    return db.query(ProjectUser).filter_by(user_id=user_id, is_deleted=False).all()
