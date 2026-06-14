from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy import CheckConstraint, Enum, ForeignKey, Index, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import SettlementStatus, enum_values


class Settlement(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "settlements"

    group_id: Mapped[UUID] = mapped_column(ForeignKey("groups.id"), nullable=False)
    paid_by: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    paid_to: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    settlement_date: Mapped[date] = mapped_column(nullable=False)
    original_amount: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    original_currency: Mapped[str] = mapped_column(String(3), nullable=False)
    base_amount: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    base_currency: Mapped[str] = mapped_column(String(3), nullable=False)
    exchange_rate: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)
    status: Mapped[SettlementStatus] = mapped_column(
        Enum(
            SettlementStatus,
            values_callable=enum_values,
            name="settlement_status",
        ),
        nullable=False,
        default=SettlementStatus.ACTIVE,
    )
    import_batch_id: Mapped[UUID | None] = mapped_column(ForeignKey("imports.id"), nullable=True)
    source_row_id: Mapped[UUID | None] = mapped_column(ForeignKey("import_rows.id"), nullable=True)
    created_by: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    group = relationship("Group", back_populates="settlements")

    __table_args__ = (
        CheckConstraint("paid_by <> paid_to", name="ck_settlements_distinct_users"),
        CheckConstraint("original_amount > 0", name="ck_settlements_original_amount_positive"),
        CheckConstraint("base_amount > 0", name="ck_settlements_base_amount_positive"),
        CheckConstraint("exchange_rate > 0", name="ck_settlements_exchange_rate_positive"),
        CheckConstraint("char_length(original_currency) = 3", name="ck_settlements_original_currency_len"),
        CheckConstraint("char_length(base_currency) = 3", name="ck_settlements_base_currency_len"),
        Index("ix_settlements_group_date", "group_id", "settlement_date"),
        Index("ix_settlements_import_source", "import_batch_id", "source_row_id"),
    )
