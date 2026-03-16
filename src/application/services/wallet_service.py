from dataclasses import dataclass
from enum import Enum
from uuid import UUID

from src.domain.entities.wallet import Wallet
from src.domain.repositories.wallet_repository import WalletRepository


class OperationType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


@dataclass
class ChangeBalanceInput:
    wallet_id: UUID
    operation_type: OperationType
    amount: int


class WalletService:
    def __init__(self, wallet_repo: WalletRepository) -> None:
        self._wallet_repo = wallet_repo

    async def get_balance(self, wallet_id: UUID) -> int:
        wallet = await self._wallet_repo.get(wallet_id)
        if wallet is None:
            return 0
        return wallet.balance

    async def change_balance(self, data: ChangeBalanceInput) -> int:
        wallet = await self._wallet_repo.get(data.wallet_id)

        if wallet is None:
            if data.operation_type is OperationType.WITHDRAW:
                raise ValueError("Wallet does not exist")
            wallet = Wallet(id=data.wallet_id, balance=0)
            await self._wallet_repo.create(wallet)

        if data.operation_type is OperationType.DEPOSIT:
            wallet.deposit(data.amount)
        else:
            wallet.withdraw(data.amount)

        await self._wallet_repo.update(wallet)
        return wallet.balance

