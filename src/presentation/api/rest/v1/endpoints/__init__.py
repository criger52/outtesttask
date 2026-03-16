from fastapi import APIRouter

from src.presentation.api.rest.v1.endpoints.change_wallet_balance import router as change_wallet_balance_router
from src.presentation.api.rest.v1.endpoints.get_wallet_balance import router as get_wallet_balance_router

api_v1_routers: tuple[APIRouter, ...] = (
    get_wallet_balance_router,
    change_wallet_balance_router,
)