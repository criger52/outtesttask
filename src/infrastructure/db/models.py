from uuid import uuid4

from sqlalchemy import BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class WalletModel(Base):
    __tablename__ = "wallets"

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    balance: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        default=0,
    )

