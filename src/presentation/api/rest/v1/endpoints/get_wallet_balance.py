from uuid import UUID

from fastapi import APIRouter

from src.presentation.api.rest.v1.schemas.wallet import WalletBalanceResponseSchema

router = APIRouter(prefix="/wallets")

@router.get("/{wallet_id}")
async def get_wallet_balance(
        wallet_id: UUID,
        wallet_service: ...,
        
) -> WalletBalanceResponseSchema:

    return