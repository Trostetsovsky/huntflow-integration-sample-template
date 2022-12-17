import logging

from hf_integration_sample.api.serializers.request.applicant_hook import (
    ApplicantHookRequest,
)
from hf_integration_sample.integrations.hf_api.client import get_client
from hf_integration_sample.integrations.hf_api import dto

logger = logging.getLogger(__name__)


async def process_applicant_hook(hook_data: ApplicantHookRequest):
    """Function for processing applicant webhook."""
    logger.info(f"Applicant webhook processor: {hook_data}")
    applicant_log = hook_data.event.applicant_log
    applicant_id = hook_data.event.applicant.id
    try:
        if applicant_log.type == "STATUS":
            if applicant_log.status.name == "Нанят":
                apiclient = get_client()
                all_organization_tags = await apiclient.get_all_tags()
                all_applicant_tags_id = await apiclient.get_all_applicant_tags(applicant_id)
                for tag in all_organization_tags:
                    if tag.name == "hired":
                        hired_tag_id = tag.id
                        if hired_tag_id not in all_applicant_tags_id.tags:
                            all_applicant_tags_id.tags.append(hired_tag_id)
                            return await apiclient.update_applicant_tags(
                                applicant_id, all_applicant_tags_id
                            )
                        else:
                            logger.info("Skip webhook, the applicant already has the 'Hired' tag")
                            return all_applicant_tags_id
                logger.info("'Hired' tag doesn't exist, create and add it to applicant")
                hired_tag = await apiclient.create_tag(dto.Tag(name="hired", color="00ad3b"))
                all_applicant_tags_id.tags.append(hired_tag.id)
                return await apiclient.update_applicant_tags(applicant_id, all_applicant_tags_id)
            else:
                logger.info("Skip webhook, status != 'Hired'")
        else:
            logger.info("Skip webhook, type of changes isn't related to the Status change")
    except AttributeError as e:
        logger.warning(f"Oops... An exception occurred while processing the applicant webhook: {e}")
