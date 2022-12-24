import logging

from hf_integration_sample.api.serializers.request.applicant_hook import (
    ApplicantHookRequest,
)
from hf_integration_sample.integrations.hf_api.client import get_client, HFAPIClient
from hf_integration_sample.integrations.hf_api import dto

logger = logging.getLogger(__name__)


class StatusNotFoundException(Exception):
    pass


async def process_applicant_hook(hook_data: ApplicantHookRequest):
    """Function for processing applicant webhook."""
    logger.info(f"Applicant webhook processor: {hook_data}")
    applicant_log = hook_data.event.applicant_log
    if applicant_log.type != "STATUS":
        logger.info("Skip webhook, type of changes isn't related to the Status change")
        return
    applicant_id = hook_data.event.applicant.id
    apiclient = get_client()
    applicant_status = await get_status_info(applicant_log.status.id, apiclient)
    if applicant_status.name != "hired":
        logger.info("Skip webhook, status != 'hired'")
        return
    hired_tag_id = await get_or_create_organization_tag("нанят", apiclient)
    all_applicant_tags_id = await apiclient.get_all_applicant_tags(applicant_id)
    if hired_tag_id in all_applicant_tags_id.tags:
        logger.info("Skip webhook, the applicant already has the 'Hired' tag")
        return all_applicant_tags_id
    all_applicant_tags_id.tags.append(hired_tag_id)
    return await apiclient.update_applicant_tags(applicant_id, all_applicant_tags_id)


async def get_or_create_organization_tag(name: str, client: HFAPIClient) -> int:
    all_tags = await client.get_all_tags()
    for tag in all_tags:
        if tag.name == name:
            return tag.id
    new_tag = await client.create_tag(dto.BaseTag(name=name, color="00ad3b"))
    return new_tag.id


async def get_status_info(status_id: int, client: HFAPIClient) -> dto.ApplicantOnVacancyStatus:
    try:
        applicant_on_vacancy_statuses = await client.get_applicant_on_vacancy_statuses()
        for status in applicant_on_vacancy_statuses:
            if status.id == status_id:
                return status
        raise StatusNotFoundException
    except StatusNotFoundException:
        logger.warning(f"StatusNotFoundException")
