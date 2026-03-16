class WalletError(Exception):
    """Base wallet domain error."""


class WalletNotFoundError(WalletError):
    """Wallet does not exist."""


class InsufficientFundsError(WalletError):
    """Balance is not enough for withdrawal."""


class InvalidAmountError(WalletError):
    """Amount is invalid (<= 0)."""

