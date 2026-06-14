from uuid import UUID

from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"

    full_name: Mapped[str] = mapped_column(String(160), nullable=False)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    preferred_currency: Mapped[str] = mapped_column(String(3), nullable=False, default="INR")

    created_groups = relationship("Group", back_populates="creator")
    memberships = relationship("GroupMembership", back_populates="user")
    paid_expenses = relationship("ExpensePayer", back_populates="user")
    expense_splits = relationship("ExpenseSplit", back_populates="user")

    __table_args__ = (
        CheckConstraint("char_length(preferred_currency) = 3", name="ck_users_preferred_currency_len"),
    )

