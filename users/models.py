# models.py
from typing import Tuple, Optional
from uuid import UUID as PyUUID, uuid4

import bcrypt
from sqlalchemy import ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from database.db import Base


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    if not email:
        return False, "Email cannot be empty"
    if "@" not in email:
        return False, "Email must contain @"
    return True, None


def validate_password(password: str) -> Tuple[bool, Optional[str]]:
    if not password:
        return False, "Password cannot be empty"
    min_length = 5
    if len(password) < min_length:
        return False, f"Password must be at least {min_length} characters long"
    return True, None


class Users(Base):
    __tablename__ = "users"

    # Основные поля
    uuid: Mapped[PyUUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    telegram: Mapped[str | None] = mapped_column(String, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Email и пароль
    _email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hash_password: Mapped[str] = mapped_column(String, nullable=False)

    # Связи
    settings: Mapped["Settings"] = relationship(
        back_populates="user", cascade="all, delete-orphan", uselist=False
    )

    # --- Гибридные свойства ---

    @hybrid_property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        if not value:
            raise ValueError("Email cannot be empty")
        is_valid, message = validate_email(value)
        if not is_valid:
            raise ValueError(f"Invalid email: {message}")
        self._email = value

    @hybrid_property
    def password(self):
        raise AttributeError("Password is not readable")

    @password.setter
    def password(self, plain_password: str):
        is_valid, message = validate_password(plain_password)
        if not is_valid:
            raise ValueError(f"Invalid password: {message}")
        hashed = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
        self.hash_password = hashed.decode("utf-8")

    def check_password(self, plain_password: str) -> bool:
        """Проверяет, совпадает ли переданный пароль с хэшем."""
        try:
            return bcrypt.checkpw(
                plain_password.encode("utf-8"), self.hash_password.encode("utf-8")
            )
        except (AttributeError, ValueError, TypeError):
            return False


class Settings(Base):
    __tablename__ = "settings"

    uuid: Mapped[PyUUID] = mapped_column(primary_key=True, default=uuid4)
    user_uuid: Mapped[PyUUID] = mapped_column(ForeignKey("users.uuid"), unique=True)
    bitrate: Mapped[str | None] = mapped_column(String, nullable=True)

    user: Mapped["Users"] = relationship(back_populates="settings")
