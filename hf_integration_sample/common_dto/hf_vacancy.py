from pydantic import BaseModel


class VacancyLogBase(BaseModel):
    id: int
    state: str


class HFVacancyBase(BaseModel):
    # Base fields set, extend it if needed
    id: int
    state: str
    position: str
