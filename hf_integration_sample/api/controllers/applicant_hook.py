import logging
from typing import Optional

from hf_integration_sample.api.serializers.request.applicant_hook import (
    ApplicantHookRequest
)
from hf_integration_sample.integrations.hf_api.client import get_client, HFAPIClient
from hf_integration_sample.integrations.hf_api.dto import UpdatedApplicantTags

logger = logging.getLogger(__name__)


async def process_applicant_hook(hook_data: ApplicantHookRequest):
    logger.info("Applicant hook processor: %s", hook_data)
    if hook_data.event.applicant_log.status.name == "Нанят":
        apiclient = get_client()
        all_tags = await apiclient.get_all_tags()
        for tag in all_tags:
            tags_id = []
            if tag.name == "hired":
                tags_id.append(tag.id)
                tmp_tags_id = UpdatedApplicantTags(tags=tags_id)
                return await apiclient.update_applicant_tags(hook_data.event.applicant.id, tmp_tags_id)
    else:
        logger.info("Skip hook, status != 'Hired'")
