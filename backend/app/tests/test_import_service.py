from uuid import uuid4

from app.models.enums import ImportStatus
from app.services.import_service import ImportService


class FakeDB:
    def __init__(self) -> None:
        self.entities = []

    def add(self, entity) -> None:
        self.entities.append(entity)

    def flush(self) -> None:
        for entity in self.entities:
            if getattr(entity, "id", None) is None:
                continue


def test_stage_csv_marks_review_required_when_anomalies_exist() -> None:
    content = "\n".join(
        [
            "date,description,paid_by,amount,currency,split_type,split_with,split_details,notes",
            "2026-02-25,Rohan paid Aisha back,Rohan,5000,INR,,Aisha,,this is a settlement not an expense??",
        ]
    )
    db = FakeDB()

    batch = ImportService(db).stage_csv(group_id=uuid4(), uploaded_by=uuid4(), file_name="expenses_export.csv", content=content)

    assert batch.status == ImportStatus.REVIEW_REQUIRED
    assert batch.report["rows_total"] == 1
    assert batch.report["anomalies"] >= 1

