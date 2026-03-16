from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.wallet import Wallet
from src.domain.repositories.wallet_repository import WalletRepository
from src.infrastructure.db.models import WalletModel


class SqlAlchemyWalletRepository(WalletRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, wallet_id: UUID) -> Optional[Wallet]:
        stmt = (
            select(WalletModel)
            .where(WalletModel.id == str(wallet_id))
            .with_for_update()
        )
        result = await self._session.execute(stmt)
        model: Optional[WalletModel] = result.scalars().first()
        if model is None:
            return None
        return Wallet(id=UUID(model.id), balance=model.balance)

    async def create(self, wallet: Wallet) -> None:
        model = WalletModel(id=str(wallet.id), balance=wallet.balance)
        self._session.add(model)

    async def update(self, wallet: Wallet) -> None:
        stmt = select(WalletModel).where(WalletModel.id == str(wallet.id))
        result = await self._session.execute(stmt)
        model: Optional[WalletModel] = result.scalars().first()
        if model is None:
            model = WalletModel(id=str(wallet.id), balance=wallet.balance)
            self._session.add(model)
        else:
            model.balance = wallet.balance

