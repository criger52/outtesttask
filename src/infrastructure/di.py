from typing import AsyncGenerator

from dishka import Provider, Scope, provide, make_async_container
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services.wallet_service import WalletService
from src.domain.repositories.wallet_repository import WalletRepository
from src.infrastructure.db.repositories import SqlAlchemyWalletRepository
from src.infrastructure.db.session import async_session_factory


class DbProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        async with async_session_factory() as session:
            async with session.begin():
                yield session


class WalletProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def wallet_repository(self, session: AsyncSession) -> WalletRepository:
        return SqlAlchemyWalletRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def wallet_service(self, wallet_repository: WalletRepository) -> WalletService:
        return WalletService(wallet_repo=wallet_repository)


container = make_async_container(DbProvider(), WalletProvider())

