from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException, status

from src.application.services.wallet_service import WalletService
from src.domain.exceptions import WalletNotFoundError
from src.presentation.api.rest.v1.schemas.wallet_balance import (
    WalletBalanceResponseSchema,
)


router = APIRouter(prefix="/wallets")

@router.get("/{wallet_id}", response_model=WalletBalanceResponseSchema)
@inject
async def get_wallet_balance(
    wallet_id: UUID,
    wallet_service: FromDishka[WalletService],
) -> WalletBalanceResponseSchema:
    try:
        balance = await wallet_service.get_balance(wallet_id)
    except WalletNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found",
        ) from None

    return WalletBalanceResponseSchema(wallet_balance=balance)

