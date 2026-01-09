# models.py
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from database.db import Base

class Track(Base):
    __tablename__ = "tracks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    object_key: Mapped[str] = mapped_column(String, unique=True)