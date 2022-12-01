from pydantic import BaseModel

from hf_integration_sample.api.serializers.request.huntflow_hook_base import (
    BaseHuntflowWebhookRequest,
)
from hf_integration_sample.common_dto.hf_applicant import HFApplicantBase, ApplicantLog


class ApplicantEvent(BaseModel):
    applicant: HFApplicantBase
    applicant_log: ApplicantLog


class ApplicantHookRequest(BaseHuntflowWebhookRequest):
    event: ApplicantEvent
