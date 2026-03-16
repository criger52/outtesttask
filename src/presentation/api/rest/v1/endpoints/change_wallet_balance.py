from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException, status

from src.application.services.wallet_service import (
    WalletService,
    ChangeBalanceInput,
    OperationType,
)
from src.domain.exceptions import (
    InvalidAmountError,
    InsufficientFundsError,
    WalletNotFoundError,
)
from src.presentation.api.rest.v1.schemas.wallet_balance import (
    WalletBalanceResponseSchema,
)
from src.presentation.api.rest.v1.schemas.wallet_operation import (
    WalletOperationRequestSchema,
)


router = APIRouter(prefix="/wallets")

@router.post("/{wallet_id}/operation", response_model=WalletBalanceResponseSchema)
@inject
async def change_wallet_balance(
    wallet_id: UUID,
    payload: WalletOperationRequestSchema,
    wallet_service: FromDishka[WalletService],
) -> WalletBalanceResponseSchema:
    try:
        operation_type = OperationType(payload.operation_type)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid operation_type",
        ) from None

    try:
        new_balance = await wallet_service.change_balance(
            ChangeBalanceInput(
                wallet_id=wallet_id,
                operation_type=operation_type,
                amount=payload.amount,
            )
        )
    except WalletNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found",
        ) from None
    except InvalidAmountError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except InsufficientFundsError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return WalletBalanceResponseSchema(wallet_balance=new_balance)

