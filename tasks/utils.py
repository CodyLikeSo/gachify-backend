import dramatiq
from users.utils import send_email_message_utility


from dramatiq.brokers.redis import RedisBroker

from global_config import TASK_DB, REDIS_PORT

url = f"redis://localhost:{REDIS_PORT}/{TASK_DB}"

broker = RedisBroker(url=url)
dramatiq.set_broker(broker)


@dramatiq.actor
def send_email(sender_email, password, receiver_email, subject, body):
    try:
        send_email_message_utility(
            sender_email=sender_email,
            password=password,
            receiver_email=receiver_email,
            subject=subject,
            body=body,
        )
    except Exception as e:
        raise e
