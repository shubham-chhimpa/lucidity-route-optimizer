import logging
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def register_handlers(app: FastAPI) -> None:
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
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})


