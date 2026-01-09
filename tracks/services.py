# services.py
import uuid
import asyncio
from tracks.models import Track
from sqlalchemy.future import select

BUCKET_NAME = "tracks"

class TrackService:
    def __init__(self, db, s3_client):
        self.db = db
        self.s3 = s3_client

    async def ensure_bucket_exists(self):
        try:
            await asyncio.to_thread(self.s3.head_bucket, Bucket=BUCKET_NAME)
        except:
            await asyncio.to_thread(self.s3.create_bucket, Bucket=BUCKET_NAME)

    async def upload_track(self, filename: str, file_data: bytes) -> Track:
        await self.ensure_bucket_exists()

        ext = filename.split('.')[-1] if '.' in filename else 'mp3'
        object_key = f"{uuid.uuid4().hex}.{ext}"

        # Загружаем в MinIO
        await asyncio.to_thread(
            self.s3.put_object,
            Bucket=BUCKET_NAME,
            Key=object_key,
            Body=file_data
        )

        # Сохраняем в БД
        track = Track(title=filename, object_key=object_key)
        self.db.add(track)
        await self.db.commit()
        await self.db.refresh(track)
        return track

    async def delete_track(self, track_id: int) -> bool:
        # Ищем трек
        result = await self.db.execute(select(Track).where(Track.id == track_id))
        track = result.scalar_one_or_none()
        if not track:
            return False

        # Удаляем из MinIO
        await asyncio.to_thread(
            self.s3.delete_object,
            Bucket=BUCKET_NAME,
            Key=track.object_key
        )

        # Удаляем из БД
        await self.db.delete(track)
        await self.db.commit()
        return True

    def get_audio_url(self, object_key: str) -> str:
        # Для фронтенда: URL для воспроизведения
        return f"http://localhost:9000/{BUCKET_NAME}/{object_key}"