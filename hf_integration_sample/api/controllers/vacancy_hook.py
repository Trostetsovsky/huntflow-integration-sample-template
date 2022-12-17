import logging

from hf_integration_sample.api.serializers.request.vacancy_hook import (
    VacancyHookRequest,
)
from hf_integration_sample.integrations.hf_api.client import get_client
from hf_integration_sample.integrations.hf_api import dto

logger = logging.getLogger(__name__)


async def process_vacancy_hook(hook_data: VacancyHookRequest):
    logger.info("Vacancy hook processor: %s", hook_data)
    vacancy_id = hook_data.event.vacancy.id
    vacancy_state = hook_data.event.vacancy_log.state
    vacancy_position = hook_data.event.vacancy.position
    try:
        if vacancy_state == "OPEN":
            logger.info(f"Vacancy in 'OPEN' status! Position {vacancy_position}.")
            apiclient = get_client()
            query_params_for_search = dto.ApplicantSearchQueryParams(
                q=vacancy_position,
                field="position",
            )
            applicants_response = await apiclient.get_applicants(
                query_params=query_params_for_search
            )
            if applicants_response.total_items > 0:
                logger.info("Found applicant, add him to the first vacancy status")
                all_vacancy_statuses = await apiclient.get_applicant_on_vacancy_statuses()
                first_applicant_id_in_response = applicants_response.items[0].id
                first_vacancy_status_id = all_vacancy_statuses[0].id
                vacancy_detail = dto.AddApplicantToTheVacancyBase(
                    vacancy=vacancy_id,
                    status=first_vacancy_status_id
                )
                return await apiclient.add_applicant_to_the_vacancy(
                    first_applicant_id_in_response,
                    vacancy_detail
                )
            else:
                logger.info("Applicants not found :(")
        else:
            logger.info("Vacancy status != 'OPEN!'")
    except AttributeError as e:
        logger.warning(f"Oops... An exception occurred while processing the applicant webhook: {e}")
