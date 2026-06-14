from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Group(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "groups"

    name: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    base_currency: Mapped[str] = mapped_column(String(3), nullable=False, default="INR")
    created_by: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    creator = relationship("User", back_populates="created_groups")
    memberships = relationship("GroupMembership", back_populates="group")
    expenses = relationship("Expense", back_populates="group")
    settlements = relationship("Settlement", back_populates="group")
    imports = relationship("ImportBatch", back_populates="group")

    __table_args__ = (
        CheckConstraint("char_length(base_currency) = 3", name="ck_groups_base_currency_len"),
    )

