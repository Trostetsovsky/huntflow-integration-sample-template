from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware import Middleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from hf_integration_sample.app.logging import configure_logging
from hf_integration_sample.app.middleware import (
    RequestIdMiddleware,
    ErrorMiddleware,
    PingMiddleware,
)
from hf_integration_sample.api.views.applicant_hook import (
    router as applicant_hook_router,
)
from hf_integration_sample.api.views.vacancy_hook import router as vacancy_hook_router
from hf_integration_sample.integrations.hf_api.client import close_client


status_router = APIRouter(tags=["health_check"])


def raise_exc(request, exc):
    """Raises an exception to bypass built-in Starlette and FastAPI error handlers"""
    raise exc


@status_router.get("/status")
def health_check():
    return {"status": "ok"}


async def shutdown():
    await close_client()


def create_app():
    configure_logging()
    app = FastAPI(
        title="hf_integration_sample",
        middleware=[
            Middleware(PingMiddleware),
            Middleware(RequestIdMiddleware),
            Middleware(ErrorMiddleware),
        ],
        exception_handlers={
            StarletteHTTPException: raise_exc,
            RequestValidationError: raise_exc,
        },
    )
    app.include_router(status_router)
    app.include_router(applicant_hook_router)
    app.include_router(vacancy_hook_router)
    app.add_event_handler("shutdown", shutdown)
    return app
