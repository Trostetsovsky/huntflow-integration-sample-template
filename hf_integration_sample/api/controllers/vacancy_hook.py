import logging
from typing import Optional

from hf_integration_sample.api.serializers.request.vacancy_hook import (
    VacancyHookRequest,
)
from hf_integration_sample.integrations.hf_api.client import get_client, HFAPIClient


logger = logging.getLogger(__name__)


async def process_vacancy_hook(hook_data: VacancyHookRequest):
    logger.info("Vacancy hook proceccor: %s", hook_data)
    # TODO: implemet
