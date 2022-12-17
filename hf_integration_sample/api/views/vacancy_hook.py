from fastapi import APIRouter, Body, Depends

from hf_integration_sample.api.controllers.vacancy_hook import process_vacancy_hook
from hf_integration_sample.api.serializers.response.hf_hook import HFHookResponse
from hf_integration_sample.api.serializers.request.vacancy_hook import (
    VacancyHookRequest,
)
from hf_integration_sample.app.hf_hooks import hf_hooks_auth


router = APIRouter(dependencies=[Depends(hf_hooks_auth)])


@router.post("/vacancy_hook", response_model=HFHookResponse)
async def applicant_hook(
    data: VacancyHookRequest = Body(..., description="Request body"),
):
    response = {"status": "ok"}
    await process_vacancy_hook(data)
    return response
