# views.py
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Query
from sqlalchemy.exc import NoResultFound
from tracks.schemas import TrackResponse, TrackUpdate
from tracks.dependencies import get_track_service
from typing import List, Optional
from fastapi.responses import StreamingResponse
import asyncio
from global_config import TRACK_BUCKET

router = APIRouter(prefix="/tracks", tags=["tracks"])


@router.post("/", response_model=TrackResponse)
async def upload_track(
    file: UploadFile = File(...), service=Depends(get_track_service)
):
    if not file.content_type.startswith("audio/"):
        raise HTTPException(400, "Only audio files allowed")

    content = await file.read()
    track = await service.upload_track(file.filename, content)

    return TrackResponse(
        id=track.id,
        title=track.title,
        audio_url=service.get_audio_url(track.object_key),
    )


@router.delete("/{track_id}")
async def delete_track(track_id: int, service=Depends(get_track_service)):
    success = await service.delete_track(track_id)
    if not success:
        raise HTTPException(404, "Track not found")
    return {"detail": "Track deleted"}


@router.get("/", response_model=List[TrackResponse])
async def list_tracks(
    service=Depends(get_track_service),
    search: Optional[str] = Query(None, description="Search by title"),
):
    tracks = await service.get_all_tracks(search=search)
    return [
        TrackResponse(
            id=track.id,
            title=track.title,
            audio_url=service.get_audio_url(track.object_key),
        )
        for track in tracks
    ]


@router.get("/{track_id}", response_model=TrackResponse)
async def get_track(track_id: int, service=Depends(get_track_service)):
    try:
        track = await service.get_track_by_id(track_id)
    except NoResultFound:
        raise HTTPException(404, "Track not found")

    return TrackResponse(
        id=track.id,
        title=track.title,
        audio_url=service.get_audio_url(track.object_key),
    )


@router.get("/{track_id}/audio")
async def stream_track_audio(track_id: int, service=Depends(get_track_service)):
    """
    Отдаёт аудиофайл напрямую с MinIO через бэкенд.
    Позволяет в будущем добавить авторизацию, логирование, рейт-лимиты.
    """
    try:
        track = await service.get_track_by_id(track_id)
    except NoResultFound:
        raise HTTPException(404, "Track not found")

    # Получаем объект из MinIO как поток
    def iterfile():
        # boto3.get_object возвращает StreamingBody
        response = service.s3_client.get_object(
            Bucket=TRACK_BUCKET, Key=track.object_key
        )
        return response["Body"].iter_chunks(chunk_size=8192)

    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None, lambda: service.s3.get_object(Bucket=TRACK_BUCKET, Key=track.object_key)
    )

    async def stream_generator():
        body = response["Body"]
        while True:
            chunk = await loop.run_in_executor(None, body.read, 8192)
            if not chunk:
                break
            yield chunk

    return StreamingResponse(stream_generator(), media_type="audio/mpeg")


@router.patch("/{track_id}", response_model=TrackResponse)
async def update_track(
    track_id: int, update_data: TrackUpdate, service=Depends(get_track_service)
):
    try:
        track = await service.update_track(track_id, update_data.title)
    except ValueError:
        raise HTTPException(404, "Track not found")

    return TrackResponse(
        id=track.id,
        title=track.title,
        audio_url=service.get_audio_url(track.object_key),
    )
