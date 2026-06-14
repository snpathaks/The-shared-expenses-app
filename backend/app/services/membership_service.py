from datetime import date
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.membership import GroupMembership
from app.repositories.memberships import MembershipRepository
from app.services.errors import ValidationError


class MembershipService:
    def __init__(self, db: Session) -> None:
        self.memberships = MembershipRepository(db)

    def require_active(self, group_id: UUID, user_id: UUID, transaction_date: date) -> GroupMembership:
        membership = self.memberships.active_on(group_id, user_id, transaction_date)
        if membership is None:
            raise ValidationError(f"User {user_id} is not active in group {group_id} on {transaction_date}")
        return membership

    def assert_all_active(self, group_id: UUID, user_ids: list[UUID], transaction_date: date) -> None:
        for user_id in user_ids:
            self.require_active(group_id, user_id, transaction_date)

