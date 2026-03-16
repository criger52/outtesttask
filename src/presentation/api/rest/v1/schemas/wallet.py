from uuid import UUID

from pydantic import BaseModel


class WalletBalanceResponseSchema(BaseModel):
    wallet_balance: float
