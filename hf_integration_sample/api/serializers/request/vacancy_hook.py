from pydantic import BaseModel

from hf_integration_sample.api.serializers.request.huntflow_hook_base import (
    BaseHuntflowWebhookRequest,
)
from hf_integration_sample.common_dto.hf_vacancy import HFVacancyBase, VacancyLogBase


class VacancyEvent(BaseModel):
    vacancy: HFVacancyBase
    vacancy_log: VacancyLogBase


class VacancyHookRequest(BaseHuntflowWebhookRequest):
    event: VacancyEvent
