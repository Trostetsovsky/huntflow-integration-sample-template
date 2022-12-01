import logging
from typing import Optional

from hf_integration_sample.api.serializers.request.applicant_hook import (
    ApplicantHookRequest,
)
from hf_integration_sample.integrations.hf_api.client import get_client, HFAPIClient


logger = logging.getLogger(__name__)


async def process_applicant_hook(hook_data: ApplicantHookRequest):
    logger.info("Applicant hook processor: %s", hook_data)
    # TODO: implement
    apiclient = get_client()
    # just print out all statuses to show usage of API client
    statuses = await apiclient.get_applicant_on_vacancy_statuses()
    print(statuses)
