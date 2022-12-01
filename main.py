import uvicorn

from hf_integration_sample.app.config import environment, Environment, settings
from hf_integration_sample.app.fastapi import create_app  # noqa


if __name__ == "__main__":
    uvicorn.run(
        "main:create_app",
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL.lower(),
        reload=environment == Environment.local,
    )
