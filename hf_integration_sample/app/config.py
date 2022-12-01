import os
from enum import Enum

from pydantic import BaseSettings


class Environment(str, Enum):
    prod = "prod"
    docker = "docker"
    local = "local"
    test = "test"


class Settings(BaseSettings):
    APP_NAME: str = "hf_integration_sample"

    PORT: int = 8000
    HOST: str = "127.0.0.1"

    TIMEOUT: int = 5
    LOG_LEVEL: str = "INFO"
    LOG_FILENAME: str = ""

    HF_API_URL: str = "https://dev-100-api.huntflow.dev"
    HF_API_TOKEN: str = ""
    HF_ORG_ACCOUNT_ID: int = 0

    SERVICE_SECRET: str = "jiechairei2Lahzo"

    class Config:
        case_sensitive = False


environment: str = os.getenv("ENVIRONMENT", Environment.local).lower()
settings = Settings(_env_file=f"config/{environment}.env")
