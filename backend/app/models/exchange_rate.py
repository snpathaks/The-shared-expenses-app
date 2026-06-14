from datetime import date
from decimal import Decimal

from sqlalchemy import CheckConstraint, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class ExchangeRate(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "exchange_rates"

    from_currency: Mapped[str] = mapped_column(String(3), nullable=False)
    to_currency: Mapped[str] = mapped_column(String(3), nullable=False)
    rate: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)
    effective_date: Mapped[date] = mapped_column(nullable=False)
    source: Mapped[str] = mapped_column(String(80), nullable=False)

    __table_args__ = (
        CheckConstraint("from_currency <> to_currency", name="ck_exchange_rates_distinct_currency"),
        CheckConstraint("rate > 0", name="ck_exchange_rates_rate_positive"),
        CheckConstraint("char_length(from_currency) = 3", name="ck_exchange_rates_from_currency_len"),
        CheckConstraint("char_length(to_currency) = 3", name="ck_exchange_rates_to_currency_len"),
        UniqueConstraint(
            "from_currency",
            "to_currency",
            "effective_date",
            "source",
            name="uq_exchange_rates_pair_date_source",
        ),
    )

