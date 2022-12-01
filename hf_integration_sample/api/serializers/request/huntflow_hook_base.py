from typing import Optional, Dict

from pydantic import BaseModel


class OrganizationAccountInfo(BaseModel):
    id: int
    name: str
    nick: str


class UserAccountInfo(BaseModel):
    id: int
    email: str
    name: str
    meta: Optional[Dict]


class WebhookMetaInfo(BaseModel):
    account: OrganizationAccountInfo
    author: UserAccountInfo
    event_id: str
    event_type: str
    retry: int
    version: str
    webhook_action: str


class BaseHuntflowWebhookRequest(BaseModel):
    changes: Optional[Dict]
    meta: WebhookMetaInfo
