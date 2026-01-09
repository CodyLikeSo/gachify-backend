# views.py
# main.py
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from tracks.schemas import TrackResponse
from tracks.dependencies import get_track_service

router = APIRouter(prefix="/tracks", tags=["tracks"])

@router.post("/post/", response_model=TrackResponse)
async def upload_track(
    file: UploadFile = File(...),
    service = Depends(get_track_service)
):
    if not file.content_type.startswith("audio/"):
        raise HTTPException(400, "Only audio files allowed")

    content = await file.read()
    track = await service.upload_track(file.filename, content)

    return TrackResponse(
        id=track.id,
        title=track.title,
        audio_url=service.get_audio_url(track.object_key)
    )

@router.delete("/delete/{track_id}")
async def delete_track(
    track_id: int,
    service = Depends(get_track_service)
):
    success = await service.delete_track(track_id)
    if not success:
        raise HTTPException(404, "Track not found")
    return {"detail": "Track deleted"}