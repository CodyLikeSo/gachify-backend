# schemas.py
from pydantic import BaseModel


class TrackCreate(BaseModel):
    title: str


class TrackResponse(BaseModel):
    id: int
    title: str
    audio_url: str

    class Config:
        from_attributes = True


class TrackListResponse(BaseModel):
    id: int
    title: str


class TrackUpdate(BaseModel):
    title: str
