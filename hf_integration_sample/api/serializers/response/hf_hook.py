from pydantic import BaseModel


class HFHookResponse(BaseModel):
    status: str
