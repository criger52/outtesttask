from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.domain.entities.wallet import Wallet


class WalletRepository(ABC):
    @abstractmethod
    async def get(self, wallet_id: UUID) -> Optional[Wallet]:
        """Get wallet for update with row-level lock, or None if not exists."""

    @abstractmethod
    async def create(self, wallet: Wallet) -> None:
        """Persist a new wallet."""

    @abstractmethod
    async def update(self, wallet: Wallet) -> None:
        """Persist existing wallet state."""

