import logging
from typing import Optional

from hf_integration_sample.api.serializers.request.applicant_hook import (
    ApplicantHookRequest
)
from hf_integration_sample.integrations.hf_api.client import get_client, HFAPIClient
from hf_integration_sample.integrations.hf_api import dto

logger = logging.getLogger(__name__)


async def process_applicant_hook(hook_data: ApplicantHookRequest):
    logger.info(f"Applicant webhook processor: {hook_data}")
    list_with_tags_id = []
    applicant_status = hook_data.event.applicant_log.status
    try:
        if applicant_status.name == "Нанят":
            apiclient = get_client()
            all_tags = await apiclient.get_all_tags()
            for tag in all_tags:
                if tag.name == "hired":
                    list_with_tags_id.append(tag.id)
            if len(list_with_tags_id) == 0:
                hired_tag = await apiclient.create_tag(
                    dto.Tag(
                        name="hired",
                        color="00ad3b"
                    )
                )
                list_with_tags_id.append(hired_tag.id)
            tmp_tags_id = dto.UpdatedApplicantTags(tags=list_with_tags_id)
            return await apiclient.update_applicant_tags(hook_data.event.applicant.id, tmp_tags_id)
    except AttributeError as e:
        logger.warning(f"Oops... An exception occurred while processing the applicant webhook: {e}")






    else:
        logger.info("Skip hook, status != 'Hired'")
