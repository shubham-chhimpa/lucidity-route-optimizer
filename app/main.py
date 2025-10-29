from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import logging
from app.models import RouteRequest, RouteResponse
from app.services import find_best_route
from app.logging_config import setup_logging

app = FastAPI(
    title="Lucidity Route Optimizer",
    description="Finds the shortest delivery route factoring in prep times.",
    version="1.0.0"
)


@app.on_event("startup")
async def _startup() -> None:
    setup_logging()
    logging.getLogger(__name__).info("Application startup complete")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.getLogger(__name__).warning("Validation error: %s", exc)
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Invalid request payload",
            "errors": exc.errors(),
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logging.getLogger(__name__).exception("Unhandled error")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


@app.get("/healthz")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/readyz")
async def ready() -> dict:
    # If later dependencies (DB, cache) are added, check them here
    return {"status": "ready"}


@app.post("/find-route", response_model=RouteResponse)
async def find_route_endpoint(request: RouteRequest):
    """
    Calculates the optimal delivery route for a batch of N orders.

    - **source**: The driver's starting location.
    - **orders**: A list of orders, each with:
        - **restaurant**: The pickup location.
        - **customer**: The dropoff location.
        - **prep_time_mins**: The meal preparation time in minutes.

    Returns the best path (as a list of location IDs) and the
    total time in minutes.
    """
    try:
        return find_best_route(request.source, request.orders)
    except ValueError as ve:
        # Surface expected bad input as 400
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception:
        # Let the global handler log and convert to 500
        raise
