from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.import_batch import ImportBatch, ImportRow
from app.repositories.base import BaseRepository


class ImportRepository(BaseRepository[ImportBatch]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, ImportBatch)

    def get_with_rows(self, import_id: UUID) -> ImportBatch | None:
        stmt = select(ImportBatch).options(selectinload(ImportBatch.rows)).where(ImportBatch.id == import_id)
        return self.db.scalar(stmt)

    def add_row(self, row: ImportRow) -> ImportRow:
        self.db.add(row)
        return row

