from fastapi import APIRouter

from app.api.v1 import balances, expenses, imports, settlements

router = APIRouter(prefix="/api/v1")
router.include_router(expenses.router)
router.include_router(settlements.router)
router.include_router(balances.router)
router.include_router(imports.router)

