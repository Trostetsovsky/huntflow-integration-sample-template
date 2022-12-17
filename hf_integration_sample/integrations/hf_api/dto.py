import datetime
from typing import List, Optional

from pydantic import BaseModel

from hf_integration_sample.common_dto.hf_applicant import HFApplicantBase, SearchApplicantsBase


class ApplicantSearchQueryParams(SearchApplicantsBase):
    pass


class ApplicantSearchResponseItem(HFApplicantBase):
    pass


class PaginatedResponseBase(BaseModel):
    page: int
    count: int
    total_pages: int
    total_items: int


class ApplicantsPaginatedSearchResponse(PaginatedResponseBase):
    items: List[ApplicantSearchResponseItem]


class ApplicantOnVacancyStatus(BaseModel):
    id: int
    name: str
    type: str


class ApplicantOnVacancyStatusCollection(BaseModel):
    items: List[ApplicantOnVacancyStatus]


class Tag(BaseModel):
    id: Optional[int]
    name: str
    color: str


class TagList(BaseModel):
    items: List[Tag]


class UpdatedApplicantTags(BaseModel):
    tags: List[int]


class AddApplicantToTheVacancyBase(BaseModel):
    vacancy: int
    status: int


class AddApplicantToTheVacancyResponse(AddApplicantToTheVacancyBase):
    id: int
    changed: datetime.datetime
    rejection_reason: Optional[int]
