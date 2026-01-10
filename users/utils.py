# utils.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from users.models import Users
from users.schemas import UsersCreate
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


async def is_user_exist(session: AsyncSession, email: str) -> bool:
    result = await session.execute(select(Users).where(Users.email == email))
    user = result.scalar_one_or_none()
    return user is not None


async def create_new_user(user_data: UsersCreate, session: AsyncSession):
    user = Users(
        email=user_data.email,
        name=user_data.name,
        telegram=user_data.telegram,
        active=user_data.active,
    )

    user.password = user_data.password

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


def send_email_message_utility(sender_email, password, receiver_email, subject, body):
    try:
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))
    except Exception as e:
        raise e

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(message)
    except Exception as e:
        raise e
