import random
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from database.db import get_db
from users.models import Users
from users.schemas import (
    UsersCreate,
    TokenResponse,
    CodeData,
    ChangePasswordRequest,
    RedisCode,
)
from jsonwebtoken.utils import encode_jwt, get_current_active_user
from users.utils import is_user_exist, create_new_user
from management.exception import (
    UserAlreadyExistHttpException,
    CantCreateUserHttpException,
    UnexpectedHttpException,
    RedisSetHttpException,
    EmailSendHttpException,
    RedisGetHttpException,
    VerificationReHttpException,
    UserNotFoundHttpException,
    UserNotVerifiedHttpException,
    InvalidPasswordHttpException,
    EmailTaskCreationHttpException,
    EmailRequiredHttpException,
    InvalidResetCodeHttpException,
    ResetCodeNotFoundHttpException,
    InvalidRedisDataHttpException,
    PasswordUpdateHttpException,
)

from redisdb.config import JOIN_PREFIX, RESET_PREFIX
from redisdb.utils import generate_key, get_redis_db
from tasks.utils import send_email
from global_config import SENDER_EMAIL as sender_email, EMAIL_PASSWORD as email_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/join/")
async def join(
    user_data: UsersCreate,
    session: AsyncSession = Depends(get_db),
    redis_client=Depends(get_redis_db("EMAIL_DB")),
):

    user = await is_user_exist(session=session, email=user_data.email)
    if user:
        raise UserAlreadyExistHttpException()

    try:
        user = await create_new_user(user_data=user_data, session=session)
    except ValueError:
        raise CantCreateUserHttpException()
    except Exception as e:
        raise UnexpectedHttpException(e=str(e))

    secret_code = str(random.randint(100000, 999999))
    redis_key = generate_key(prefix=JOIN_PREFIX, sub=user.email)
    value_dict = RedisCode(code=secret_code, email=user.email, user=user.name)

    try:
        await redis_client.setex(
            name=redis_key, time=300, value=value_dict.model_dump_json()
        )
    except Exception:
        raise RedisSetHttpException()

    try:
        task = send_email.send(
            sender_email=sender_email,
            password=email_password,
            receiver_email=user.email,
            subject="Secret code",
            body=f"Your verification code: {secret_code}",
        )

        if not task:
            await redis_client.delete(redis_key)
            raise UnexpectedHttpException(e="")

    except Exception as e:
        await redis_client.delete(redis_key)

        raise EmailSendHttpException(e=str(e))

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Verification code sent to your email",
            "task_id": str(task.message_id),
            "queue": "default",
        },
    )


@router.post("/verify-email/")
async def verify_email(
    data: CodeData,
    session: AsyncSession = Depends(get_db),
    redis_client=Depends(get_redis_db("EMAIL_DB")),
):
    key = generate_key(prefix=JOIN_PREFIX, sub=data.email)

    try:
        result = await redis_client.get(key)
    except Exception:
        raise RedisGetHttpException()

    if not result:
        raise RedisGetHttpException()

    try:
        redis_data = RedisCode.model_validate_json(result)

        if data.code == str(redis_data.code):
            await redis_client.delete(key)

            user_result = await session.execute(
                select(Users).where(Users.email == data.email)
            )
            user = user_result.scalar_one_or_none()

            if user:
                user.active = True
                await session.commit()

            return JSONResponse(
                status_code=200,
                content={"status": "success", "detail": "Email verified successfully"},
            )
        else:
            raise VerificationReHttpException()

    except ValidationError as e:
        raise UnexpectedHttpException(e=e)


@router.post("/login/", response_model=TokenResponse)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_db),
):
    try:
        response = await session.execute(
            select(Users).where(Users.name == form_data.username)
        )
        user = response.scalar_one_or_none()

        if not user:
            raise UserNotFoundHttpException()

        if not user.active:
            raise UserNotVerifiedHttpException()

        password_valid = user.check_password(form_data.password)

        if not password_valid:
            raise InvalidPasswordHttpException()

        payload = {
            "sub": user.name,
            "email": user.email,
            "uuid": str(user.uuid),
            "exp": datetime.now(timezone.utc) + timedelta(hours=24),
        }

        token = encode_jwt(payload=payload)

        return TokenResponse(access_token=token, token_type="Bearer")

    except (
        UserNotFoundHttpException,
        UserNotVerifiedHttpException,
        InvalidPasswordHttpException,
    ):
        raise
    except Exception as e:
        raise UnexpectedHttpException(e=str(e))


@router.get("/reset_password/")
async def reset_password(
    user: Users = Depends(get_current_active_user),
    redis_client=Depends(get_redis_db("EMAIL_DB")),
):
    if not user.email:
        raise EmailRequiredHttpException()

    reset_code = str(random.randint(100000, 999999))

    try:
        value_dict = RedisCode(code=reset_code, email=user.email, user=user.name)

        redis_key = generate_key(prefix=RESET_PREFIX, sub=user.email)

        await redis_client.setex(
            name=redis_key,
            time=300,  # 5 минут
            value=value_dict.model_dump_json(),  # Используем Pydantic сериализацию
        )
    except Exception as e:
        raise RedisSetHttpException(e=str(e))

    try:
        task = send_email.send(
            sender_email=sender_email,
            password=email_password,
            receiver_email=user.email,
            subject="Password Reset Code",
            body=f"Your password reset code: {reset_code}\nThis code will expire in 5 minutes.",
        )

        if not task:
            await redis_client.delete(redis_key)
            raise EmailTaskCreationHttpException()

    except Exception as e:
        try:
            await redis_client.delete(redis_key)
        except Exception:
            pass

        raise EmailSendHttpException(e=str(e))

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Password reset code sent to your email",
            "task_id": str(task.message_id),
            "queue": "default",
        },
    )


@router.post("/change-password/")
async def change_password(
    password_data: ChangePasswordRequest,
    user: Users = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db),
    redis_client=Depends(get_redis_db("EMAIL_DB")),
):
    if not user.email:
        raise EmailRequiredHttpException()

    try:
        redis_key = generate_key(prefix=RESET_PREFIX, sub=user.email)
        data = await redis_client.get(redis_key)

        if not data:
            raise ResetCodeNotFoundHttpException()

        value_dict = RedisCode.model_validate_json(data)
        stored_code = value_dict.code

        if stored_code != str(password_data.code):
            raise InvalidResetCodeHttpException()

    except (ResetCodeNotFoundHttpException, InvalidResetCodeHttpException):
        raise
    except ValidationError as e:
        raise InvalidRedisDataHttpException(e=str(e))
    except Exception as e:
        raise RedisGetHttpException(e=str(e))

    try:
        user.password = password_data.new_password
        session.add(user)
        await session.commit()

    except Exception as e:
        await session.rollback()
        raise PasswordUpdateHttpException(e=str(e))

    try:
        if redis_key:
            await redis_client.delete(redis_key)
    except Exception as e:
        UnexpectedHttpException(e=str(e))

    return JSONResponse(
        status_code=200,
        content={"status": "success", "message": "Password updated successfully"},
    )
