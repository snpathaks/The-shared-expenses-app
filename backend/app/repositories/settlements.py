from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import SettlementStatus
from app.models.settlement import Settlement
from app.repositories.base import BaseRepository


class SettlementRepository(BaseRepository[Settlement]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Settlement)

    def list_active_for_group(self, group_id: UUID) -> list[Settlement]:
        stmt = (
            select(Settlement)
            .where(Settlement.group_id == group_id, Settlement.status == SettlementStatus.ACTIVE)
            .order_by(Settlement.settlement_date, Settlement.created_at)
        )
        return list(self.db.scalars(stmt))

