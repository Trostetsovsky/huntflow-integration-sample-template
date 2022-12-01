import logging
from functools import lru_cache
from typing import List, Optional

import httpx

from hf_integration_sample.integrations.hf_api import dto
from hf_integration_sample.app.config import settings


logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 10


class HFAPIClient:
    api_prefix = "/v2"
    org_account_prefix = api_prefix + "/accounts/{}"

    def __init__(self, api_base: str, token: str, org_account_id: int):
        self.api_base = api_base
        self.token = token
        self.org_account_id = org_account_id
        self.http_client = httpx.AsyncClient(
            headers=self.get_auth_headers(), timeout=DEFAULT_TIMEOUT
        )

    async def close(self):
        await self.http_client.aclose()

    def get_auth_headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    async def request(self, method, url, **kwargs):
        logger.info("Sending request '%s' to %s", method, url)
        response = await self.http_client.request(method, url, **kwargs)
        logger.info("Response %s", response.status_code)
        response.raise_for_status()
        return response

    def get_org_bound_url(self, path):
        assert self.org_account_id
        return self.api_base + self.org_account_prefix.format(self.org_account_id) + path

    async def get_applicant_on_vacancy_statuses(
        self,
    ) -> List[dto.ApplicantOnVacancyStatus]:
        """Incapsulates API call to get all applicant on vacancy statuses.
        Working method, you may use it as an example to implement another API calls.
        """
        path = "/vacancies/statuses"
        url = self.get_org_bound_url(path)
        response = await self.request("GET", url)
        data = dto.ApplicantOnVacancyStatusCollection.parse_obj(response.json())
        return data.items


@lru_cache(1)
def get_client() -> HFAPIClient:
    return HFAPIClient(
        settings.HF_API_URL,
        settings.HF_API_TOKEN,
        settings.HF_ORG_ACCOUNT_ID,
    )


async def close_client():
    await get_client().close()
