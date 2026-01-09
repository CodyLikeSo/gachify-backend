from uuid import UUID
from pydantic import BaseModel


class UserJoinEvent(BaseModel):
    status: str = "ok"
    action: str
    user_id: UUID | str
    email: str


class UserLoginEvent(BaseModel):
    status: str = "ok"
    action: str
    user_id: UUID | str
    email: str
    access_token: str