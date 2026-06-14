from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.group import Group
from app.models.membership import GroupMembership
from app.repositories.base import BaseRepository


class GroupRepository(BaseRepository[Group]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Group)

    def list_for_user(self, user_id: UUID) -> list[Group]:
        stmt = (
            select(Group)
            .join(GroupMembership, GroupMembership.group_id == Group.id)
            .where(GroupMembership.user_id == user_id)
            .order_by(Group.created_at.desc())
        )
        return list(self.db.scalars(stmt).unique())

