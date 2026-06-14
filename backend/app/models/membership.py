from datetime import date
from uuid import UUID

from sqlalchemy import CheckConstraint, Enum, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import MembershipRole, enum_values


class GroupMembership(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "group_memberships"

    group_id: Mapped[UUID] = mapped_column(ForeignKey("groups.id"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    role: Mapped[MembershipRole] = mapped_column(
        Enum(
            MembershipRole,
            values_callable=enum_values,
            name="membership_role",
        ),
        nullable=False,
    )
    joined_at: Mapped[date] = mapped_column(nullable=False)
    left_at: Mapped[date | None] = mapped_column(nullable=True)

    group = relationship("Group", back_populates="memberships")
    user = relationship("User", back_populates="memberships")

    __table_args__ = (
        CheckConstraint("left_at IS NULL OR left_at > joined_at", name="ck_membership_valid_interval"),
        Index("ix_memberships_group_user_dates", "group_id", "user_id", "joined_at", "left_at"),
        UniqueConstraint("group_id", "user_id", "joined_at", name="uq_membership_group_user_joined"),
    )
