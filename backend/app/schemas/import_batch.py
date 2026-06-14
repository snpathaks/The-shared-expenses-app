from uuid import UUID

from pydantic import BaseModel

from app.schemas.common import ORMModel


class ImportRead(ORMModel):
    id: UUID
    file_name: str
    status: str
    report: dict


class ImportUploadResponse(BaseModel):
    import_id: UUID
    status: str
    report: dict

