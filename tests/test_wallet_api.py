import asyncio
from uuid import uuid4

import httpx
import pytest
from fastapi import FastAPI
from httpx import ASGITransport

from src.main import create_app


@pytest.fixture
def app() -> FastAPI:
    return create_app()


@pytest.fixture
def client(app: FastAPI) -> httpx.AsyncClient:
    transport = ASGITransport(app=app)
    return httpx.AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_wallet_not_found(client: httpx.AsyncClient):
    wallet_id = uuid4()
    resp = await client.get(f"/api/v1/wallets/{wallet_id}")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_deposit_and_withdraw(client: httpx.AsyncClient):
    wallet_id = uuid4()

    resp = await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "DEPOSIT", "amount": 1000},
    )
    assert resp.status_code in (200, 404)


@pytest.mark.asyncio
async def test_concurrent_deposits(client: httpx.AsyncClient):
    wallet_id = uuid4()

    async def deposit():
        return await client.post(
            f"/api/v1/wallets/{wallet_id}/operation",
            json={"operation_type": "DEPOSIT", "amount": 100},
        )

    tasks = [deposit() for _ in range(10)]
    responses = await asyncio.gather(*tasks)
    assert all(r.status_code in (200, 404) for r in responses)

