from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import current_user_id, db_session
from app.schemas.import_batch import ImportUploadResponse
from app.services.import_service import ImportService

router = APIRouter(prefix="/groups/{group_id}/imports", tags=["imports"])


@router.post("", response_model=ImportUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_import(
    group_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(db_session),
    actor_id: UUID = Depends(current_user_id),
) -> ImportUploadResponse:
    raw = await file.read()
    content = raw.decode("utf-8-sig")
    batch = ImportService(db).stage_csv(
        group_id=group_id,
        uploaded_by=actor_id,
        file_name=file.filename or "upload.csv",
        content=content,
    )
    db.commit()
    db.refresh(batch)
    return ImportUploadResponse(import_id=batch.id, status=batch.status.value, report=batch.report)

