# dependencies.py
import asyncio
import boto3
from fastapi import Depends
from database.db import get_db
from global_config import MINIO_ADMIN, MINIO_HOST, MINIO_PASSWORD, MINIO_PORT, TRACK_BUCKET
from tracks.services import TrackService


def get_minio_client():
    return boto3.client(
        "s3",
        endpoint_url=f"http://{MINIO_HOST}:{MINIO_PORT}",
        aws_access_key_id=MINIO_ADMIN,
        aws_secret_access_key=MINIO_PASSWORD,
        region_name="us-east-1"
    )

async def init_minio():
    s3 = get_minio_client()
    try:
        await asyncio.to_thread(s3.head_bucket, Bucket=TRACK_BUCKET)
        print(f"Bucket '{TRACK_BUCKET}' already exists.")
    except Exception as e:
        print(f"Bucket '{TRACK_BUCKET}' not found. Creating...")
        await asyncio.to_thread(s3.create_bucket, Bucket=TRACK_BUCKET)
        print(f"Bucket '{TRACK_BUCKET}' created successfully.")


async def get_track_service(
    db = Depends(get_db),
    s3_client = Depends(get_minio_client)
):
    return TrackService(db=db, s3_client=s3_client)



