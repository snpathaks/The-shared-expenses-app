from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.membership import GroupMembership
from app.repositories.base import BaseRepository


class MembershipRepository(BaseRepository[GroupMembership]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, GroupMembership)

    def active_on(self, group_id: UUID, user_id: UUID, transaction_date: date) -> GroupMembership | None:
        stmt = select(GroupMembership).where(
            GroupMembership.group_id == group_id,
            GroupMembership.user_id == user_id,
            GroupMembership.joined_at <= transaction_date,
            (GroupMembership.left_at.is_(None)) | (GroupMembership.left_at > transaction_date),
        )
        return self.db.scalar(stmt)

    def list_group_memberships(self, group_id: UUID) -> list[GroupMembership]:
        stmt = select(GroupMembership).where(GroupMembership.group_id == group_id).order_by(GroupMembership.joined_at)
        return list(self.db.scalars(stmt))

