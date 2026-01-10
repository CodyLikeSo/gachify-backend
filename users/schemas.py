# schemas.py
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr


class SettingsBase(BaseModel):
    bitrate: Optional[str] = None


class SettingsRead(SettingsBase):
    uuid: UUID
    user_uuid: UUID

    class Config:
        from_attributes = True


class UsersCreate(BaseModel):
    email: EmailStr  # ← добавлено
    password: str = Field(..., min_length=5)  # ← добавлено
    name: Optional[str] = None
    telegram: Optional[str] = None
    active: bool = False


class UsersModify(BaseModel):
    # Обновление профиля — без email и пароля (они меняются отдельно)
    name: Optional[str] = None
    telegram: Optional[str] = None
    active: Optional[bool] = None


class UsersReplace(UsersModify):
    pass


class UserRead(BaseModel):
    uuid: UUID
    email: EmailStr  # ← добавлено
    name: Optional[str] = None
    telegram: Optional[str] = None
    active: bool = False
    settings: Optional[SettingsRead] = None

    class Config:
        from_attributes = True


class UsersList(BaseModel):
    uuid: UUID
    name: Optional[str]
    telegram: Optional[str]
    active: bool

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class CodeData(BaseModel):
    code: str
    email: EmailStr  # ← улучшена валидация


class ChangePasswordRequest(BaseModel):
    code: str
    new_password: str = Field(..., min_length=5)  # ← добавлена минимальная длина


class RedisCode(BaseModel):
    code: str
    email: EmailStr  # ← улучшена валидация
    user: str
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class TokenData(BaseModel):
    name: str
