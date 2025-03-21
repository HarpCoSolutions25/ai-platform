import uuid
from sqlmodel import Session, select, delete, func
from app.models import ProjectUser, ProjectUserPublic, User
from datetime import datetime


def is_project_admin(session: Session, user_id: str, project_id: int) -> bool:
    """
    Checks if a user is an admin of the given project.
    """
    project_user = session.exec(
        select(ProjectUser).where(
            ProjectUser.project_id == project_id,
            ProjectUser.user_id == user_id,
            ProjectUser.is_deleted == False
        )
    ).first()

    return bool(project_user and project_user.is_admin)

# Add a user to a project
def add_user_to_project(
    session: Session, project_id: uuid.UUID, user_id: uuid.UUID, is_admin: bool = False
) -> ProjectUserPublic:
    """
    Adds a user to a project.
    """
    existing = session.exec(
        select(ProjectUser).where(ProjectUser.project_id == project_id, ProjectUser.user_id == user_id)
    ).first()

    if existing:
        raise ValueError("User is already a member of this project.")

    project_user = ProjectUser(project_id=project_id, user_id=user_id, is_admin=is_admin)
    session.add(project_user)
    session.commit()
    session.refresh(project_user)

    return ProjectUserPublic.model_validate(project_user)


def remove_user_from_project(session: Session, project_id: uuid.UUID, user_id: uuid.UUID) -> None:
    """
    Removes a user from a project.
    """
    project_user = session.exec(
        select(ProjectUser).where(
            ProjectUser.project_id == project_id,
            ProjectUser.user_id == user_id,
            ProjectUser.is_deleted == False  # Ignore already deleted users
        )
    ).first()
    if not project_user:
        raise ValueError("User is not a member of this project or already removed.")
    
    project_user.is_deleted = True
    project_user.deleted_at = datetime.utcnow()
    session.add(project_user)  # Required to mark as dirty for commit
    session.commit()


def get_users_by_project(
    session: Session, project_id: uuid.UUID, skip: int = 0, limit: int = 100
) -> tuple[list[ProjectUserPublic], int]:
    """
    Returns paginated users in a given project along with the total count.
    """
    count_statement = select(func.count()).select_from(ProjectUser).where(
        ProjectUser.project_id == project_id, ProjectUser.is_deleted == False
    )
    total_count = session.exec(count_statement).one()

    statement = (
        select(ProjectUser)
        .where(ProjectUser.project_id == project_id, ProjectUser.is_deleted == False)
        .offset(skip)
        .limit(limit)
    )
    users = session.exec(statement).all()

    return [ProjectUserPublic.model_validate(user) for user in users], total_count
