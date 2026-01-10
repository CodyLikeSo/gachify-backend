import jwt
from pathlib import Path
from typing import Annotated
from fastapi import Depends, HTTPException
from sqlalchemy import select
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from database.db import get_db
from users.models import Users
from users.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


def encode_jwt(payload: dict) -> str:
    private_key_path = Path(__file__).parent / "certs" / "jwt-private.pem"
    try:
        with open(private_key_path, "r") as key_file:
            private_key = key_file.read()
    except FileNotFoundError:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="JWT private key not found",
        )

    return jwt.encode(payload=payload, key=private_key, algorithm="RS256")


def decode_jwt(token: str) -> dict:
    public_key_path = Path(__file__).parent / "creds" / "jwt-public.pem"
    try:
        with open(public_key_path, "r") as key_file:
            public_key = key_file.read()
    except FileNotFoundError:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="JWT public key not found",
        )

    try:
        return jwt.decode(token, key=public_key, algorithms=["RS256"])
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_jwt(token)
        uuid: str = payload.get("sub")
        if uuid is None:
            raise credentials_exception
        token_data = TokenData(uuid=uuid)
    except Exception:
        raise credentials_exception

    response = await session.execute(select(Users).where(Users.uuid == token_data.uuid))
    user = response.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Users = Depends(get_current_user)):
    return current_user
