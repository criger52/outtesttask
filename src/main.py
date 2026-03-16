from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka

from src.infrastructure.di import container
from src.presentation.api.rest.v1.endpoints import api_v1_routers


def create_app() -> FastAPI:
    app = FastAPI(title="Wallet Service")
    setup_dishka(container=container, app=app)
    for router in api_v1_routers:
        app.include_router(router)
    return app


app = create_app()

