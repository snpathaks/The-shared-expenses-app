from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy import CheckConstraint, Enum, ForeignKey, Index, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import ExpenseStatus, SplitType, enum_values


class Expense(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "expenses"

    group_id: Mapped[UUID] = mapped_column(ForeignKey("groups.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(240), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    expense_date: Mapped[date] = mapped_column(nullable=False)
    original_amount: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    original_currency: Mapped[str] = mapped_column(String(3), nullable=False)
    base_amount: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    base_currency: Mapped[str] = mapped_column(String(3), nullable=False)
    exchange_rate: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)
    split_type: Mapped[SplitType] = mapped_column(
        Enum(
            SplitType,
            values_callable=enum_values,
            name="split_type",
        ),
        nullable=False,
    )
    status: Mapped[ExpenseStatus] = mapped_column(
        Enum(
            ExpenseStatus,
            values_callable=enum_values,
            name="expense_status",
        ),
        nullable=False,
        default=ExpenseStatus.ACTIVE,
    )
    import_batch_id: Mapped[UUID | None] = mapped_column(ForeignKey("imports.id"), nullable=True)
    source_row_id: Mapped[UUID | None] = mapped_column(ForeignKey("import_rows.id"), nullable=True)
    created_by: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    group = relationship("Group", back_populates="expenses")
    payers = relationship("ExpensePayer", back_populates="expense", cascade="all, delete-orphan")
    splits = relationship("ExpenseSplit", back_populates="expense", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("original_amount >= 0", name="ck_expenses_original_amount_non_negative"),
        CheckConstraint("base_amount >= 0", name="ck_expenses_base_amount_non_negative"),
        CheckConstraint("exchange_rate > 0", name="ck_expenses_exchange_rate_positive"),
        CheckConstraint("char_length(original_currency) = 3", name="ck_expenses_original_currency_len"),
        CheckConstraint("char_length(base_currency) = 3", name="ck_expenses_base_currency_len"),
        Index("ix_expenses_group_date", "group_id", "expense_date"),
        Index("ix_expenses_import_source", "import_batch_id", "source_row_id"),
    )


class ExpensePayer(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "expense_payers"

    expense_id: Mapped[UUID] = mapped_column(ForeignKey("expenses.id"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    base_amount: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)

    expense = relationship("Expense", back_populates="payers")
    user = relationship("User", back_populates="paid_expenses")

    __table_args__ = (
        CheckConstraint("amount >= 0", name="ck_expense_payers_amount_non_negative"),
        CheckConstraint("base_amount >= 0", name="ck_expense_payers_base_amount_non_negative"),
        CheckConstraint("char_length(currency) = 3", name="ck_expense_payers_currency_len"),
        Index("ix_expense_payers_expense_user", "expense_id", "user_id"),
    )


class ExpenseSplit(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "expense_splits"

    expense_id: Mapped[UUID] = mapped_column(ForeignKey("expenses.id"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    split_amount: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    base_amount: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    percentage: Mapped[Decimal | None] = mapped_column(Numeric(9, 6), nullable=True)
    shares: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)

    expense = relationship("Expense", back_populates="splits")
    user = relationship("User", back_populates="expense_splits")

    __table_args__ = (
        CheckConstraint("split_amount >= 0", name="ck_expense_splits_amount_non_negative"),
        CheckConstraint("base_amount >= 0", name="ck_expense_splits_base_amount_non_negative"),
        CheckConstraint("percentage IS NULL OR percentage >= 0", name="ck_expense_splits_percentage_non_negative"),
        CheckConstraint("shares IS NULL OR shares >= 0", name="ck_expense_splits_shares_non_negative"),
        CheckConstraint("char_length(currency) = 3", name="ck_expense_splits_currency_len"),
        Index("ix_expense_splits_expense_user", "expense_id", "user_id"),
    )
