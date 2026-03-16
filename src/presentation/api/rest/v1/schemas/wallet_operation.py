from pydantic import BaseModel, Field, ConfigDict


class WalletOperationRequestSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        frozen=True,
    )
    operation_type: str
    amount: int = Field(..., gt=0)

