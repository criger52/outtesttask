from pydantic import BaseModel, Field, ConfigDict


class WalletBalanceResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        frozen=True,
    )
    wallet_balance: int

