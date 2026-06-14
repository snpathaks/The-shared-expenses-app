from uuid import UUID

from sqlalchemy import Enum, ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import ImportRowDecision, ImportRowParseStatus, ImportStatus, enum_values


class ImportBatch(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "imports"

    group_id: Mapped[UUID] = mapped_column(ForeignKey("groups.id"), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[ImportStatus] = mapped_column(
        Enum(
            ImportStatus,
            values_callable=enum_values,
            name="import_status",
        ),
        nullable=False,
    )
    uploaded_by: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    report: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    group = relationship("Group", back_populates="imports")
    rows = relationship("ImportRow", back_populates="import_batch", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_imports_group_status", "group_id", "status"),
        UniqueConstraint("group_id", "file_hash", name="uq_imports_group_file_hash"),
    )


class ImportRow(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "import_rows"

    import_id: Mapped[UUID] = mapped_column(ForeignKey("imports.id"), nullable=False)
    row_number: Mapped[int] = mapped_column(Integer, nullable=False)
    raw_data: Mapped[dict] = mapped_column(JSONB, nullable=False)
    row_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    parse_status: Mapped[ImportRowParseStatus] = mapped_column(
        Enum(
            ImportRowParseStatus,
            values_callable=enum_values,
            name="import_row_parse_status",
        ),
        nullable=False,
    )
    parse_errors: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    normalized_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_expense_id: Mapped[UUID | None] = mapped_column(ForeignKey("expenses.id"), nullable=True)
    created_settlement_id: Mapped[UUID | None] = mapped_column(ForeignKey("settlements.id"), nullable=True)
    decision: Mapped[ImportRowDecision] = mapped_column(
        Enum(
            ImportRowDecision,
            values_callable=enum_values,
            name="import_row_decision",
        ),
        nullable=False,
        default=ImportRowDecision.PENDING,
    )

    import_batch = relationship("ImportBatch", back_populates="rows")
    anomalies = relationship("Anomaly", back_populates="import_row", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("import_id", "row_number", name="uq_import_rows_import_row_number"),
        Index("ix_import_rows_row_hash", "row_hash"),
        Index("ix_import_rows_import_decision", "import_id", "decision"),
    )
