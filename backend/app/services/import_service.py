import csv
import hashlib
import logging
from io import StringIO
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.anomaly import Anomaly
from app.models.enums import AnomalyStatus, ImportRowDecision, ImportRowParseStatus, ImportStatus
from app.models.import_batch import ImportBatch, ImportRow
from app.repositories.imports import ImportRepository
from app.services.anomaly_service import AnomalyService

logger = logging.getLogger(__name__)


class ImportService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.imports = ImportRepository(db)
        self.anomalies = AnomalyService()

    def stage_csv(self, *, group_id: UUID, uploaded_by: UUID, file_name: str, content: str) -> ImportBatch:
        file_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        batch = ImportBatch(
            group_id=group_id,
            file_name=file_name,
            file_hash=file_hash,
            status=ImportStatus.STAGED,
            uploaded_by=uploaded_by,
            report={},
        )
        self.db.add(batch)
        self.db.flush()

        rows_total = 0
        anomaly_count = 0
        reader = csv.DictReader(StringIO(content))
        for row_number, row in enumerate(reader, start=1):
            rows_total += 1
            row_hash = hashlib.sha256(str(sorted(row.items())).encode("utf-8")).hexdigest()
            import_row = ImportRow(
                import_id=batch.id,
                row_number=row_number,
                raw_data=row,
                row_hash=row_hash,
                parse_status=ImportRowParseStatus.PARSED,
                parse_errors=[],
                normalized_data=None,
                decision=ImportRowDecision.PENDING,
            )
            self.db.add(import_row)
            self.db.flush()

            for finding in self.anomalies.inspect_row(row_number, row):
                anomaly_count += 1
                self.db.add(
                    Anomaly(
                        import_id=batch.id,
                        import_row_id=import_row.id,
                        entity_type="import_row",
                        rule_code=finding.rule_code,
                        severity=finding.severity,
                        message=finding.message,
                        details=finding.details,
                        status=AnomalyStatus.OPEN,
                        requires_approval=finding.requires_approval,
                    )
                )

        batch.status = ImportStatus.REVIEW_REQUIRED if anomaly_count else ImportStatus.STAGED
        batch.report = {"rows_total": rows_total, "anomalies": anomaly_count}
        logger.info("staged import", extra={"import_id": str(batch.id), "rows_total": rows_total})
        return batch

