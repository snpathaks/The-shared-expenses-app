from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy.orm import Session

ModelT = TypeVar("ModelT")


class NotFoundError(ValueError):
    pass


class BaseRepository(Generic[ModelT]):
    def __init__(self, db: Session, model: type[ModelT]) -> None:
        self.db = db
        self.model = model

    def get(self, entity_id: UUID) -> ModelT | None:
        return self.db.get(self.model, entity_id)

    def require(self, entity_id: UUID) -> ModelT:
        entity = self.get(entity_id)
        if entity is None:
            raise NotFoundError(f"{self.model.__name__} not found: {entity_id}")
        return entity

    def add(self, entity: ModelT) -> ModelT:
        self.db.add(entity)
        return entity

