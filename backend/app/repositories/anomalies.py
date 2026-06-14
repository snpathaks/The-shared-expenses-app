from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.anomaly import Anomaly
from app.models.enums import AnomalyStatus
from app.repositories.base import BaseRepository


class AnomalyRepository(BaseRepository[Anomaly]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Anomaly)

    def list_open_for_import(self, import_id: UUID) -> list[Anomaly]:
        stmt = (
            select(Anomaly)
            .where(Anomaly.import_id == import_id, Anomaly.status == AnomalyStatus.OPEN)
            .order_by(Anomaly.created_at, Anomaly.rule_code)
        )
        return list(self.db.scalars(stmt))

