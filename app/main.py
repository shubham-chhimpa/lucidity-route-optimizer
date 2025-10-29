from fastapi import FastAPI
from app.api.routers.routes import router as route_router
from app.api.errors import register_handlers
from app.infrastructure.logging.config import setup_logging

app = FastAPI(
    title="Lucidity Route Optimizer",
    description="Finds the shortest delivery route factoring in prep times.",
    version="1.0.0"
)


@app.on_event("startup")
async def _startup() -> None:
    setup_logging()


register_handlers(app)


@app.get("/healthz")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/readyz")
async def ready() -> dict:
    return {"status": "ready"}


app.include_router(route_router)
