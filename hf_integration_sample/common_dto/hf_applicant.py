from typing import Optional

from pydantic import BaseModel


class VacancyApplicantStatus(BaseModel):
    id: int
    name: str


class ApplicantLog(BaseModel):
    id: int
    type: str
    status: Optional[VacancyApplicantStatus]


class HFApplicantBase(BaseModel):
    id: int
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    position: Optional[str]
