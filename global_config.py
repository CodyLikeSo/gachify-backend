from dotenv import load_dotenv
from pathlib import Path
import os

project_root = Path(__file__).parent.parent
dotenv_path = project_root / ".env"

load_dotenv(dotenv_path=dotenv_path)

TASK_DB = 1

# Postgres
user = os.getenv("POSTGRES_DB_USER")
password = os.getenv("POSTGRES_DB_PASSWORD")
host = os.getenv("POSTGRES_DB_HOST")
port = os.getenv("POSTGRES_DB_PORT")
database = os.getenv("POSTGRES_DB_DBNAME")
test_database = os.getenv("POSTGRES_TESTDB_DBNAME")

# Redis & Email
REDIS_PORT = os.getenv("REDIS_PORT")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# MiniO
MINIO_PORT = os.getenv("MINIO_PORT")
MINIO_WEB_PORT = os.getenv("MINIO_WEB_PORT")
MINIO_HOST = os.getenv("MINIO_HOST")
MINIO_ADMIN = os.getenv("MINIO_ADMIN")
MINIO_PASSWORD = os.getenv("MINIO_PASSWORD")
TRACK_BUCKET = os.getenv("TRACK_BUCKET")
