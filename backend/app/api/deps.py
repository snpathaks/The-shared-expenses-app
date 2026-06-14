from uuid import UUID

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db


def db_session(db: Session = Depends(get_db)) -> Session:
    return db


def current_user_id(x_user_id: UUID | None = Header(default=None, alias="X-User-Id")) -> UUID:
    if x_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-User-Id test header; replace with JWT dependency in auth increment",
        )
    return x_user_id

