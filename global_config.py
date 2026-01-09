from dotenv import load_dotenv
from pathlib import Path
import os

project_root = Path(__file__).parent.parent
dotenv_path = project_root / ".env"

load_dotenv(dotenv_path=dotenv_path)

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