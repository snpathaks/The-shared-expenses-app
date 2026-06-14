from uuid import UUID

from sqlalchemy import Boolean, Enum, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import AnomalySeverity, AnomalyStatus, enum_values


class Anomaly(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "anomalies"

    import_id: Mapped[UUID | None] = mapped_column(ForeignKey("imports.id"), nullable=True)
    import_row_id: Mapped[UUID | None] = mapped_column(ForeignKey("import_rows.id"), nullable=True)
    entity_type: Mapped[str] = mapped_column(String(80), nullable=False)
    entity_id: Mapped[UUID | None] = mapped_column(nullable=True)
    rule_code: Mapped[str] = mapped_column(String(80), nullable=False)
    severity: Mapped[AnomalySeverity] = mapped_column(
        Enum(
            AnomalySeverity,
            values_callable=enum_values,
            name="anomaly_severity",
        ),
        nullable=False,
    )
    message: Mapped[str] = mapped_column(Text, nullable=False)
    details: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    status: Mapped[AnomalyStatus] = mapped_column(
        Enum(
            AnomalyStatus,
            values_callable=enum_values,
            name="anomaly_status",
        ),
        nullable=False,
        default=AnomalyStatus.OPEN,
    )
    requires_approval: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    resolved_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    import_row = relationship("ImportRow", back_populates="anomalies")

    __table_args__ = (
        Index("ix_anomalies_import_status", "import_id", "status"),
        Index("ix_anomalies_rule_severity", "rule_code", "severity"),
    )
