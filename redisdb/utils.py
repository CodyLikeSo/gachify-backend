from redisdb.config import EMAIL_DB, TASK_DB, REGISTRATION_DB, LOGIN_DB
from global_config import host, REDIS_PORT
import redis.asyncio as redis


def generate_key(prefix, sub):
    return f"{prefix}:{sub}"


redis_clients = {}


async def init_redis():
    dbs = {
        "EMAIL_DB": EMAIL_DB,
        "TASK_DB": TASK_DB,
        "REGISTRATION_DB": REGISTRATION_DB,
        "LOGIN_DB": LOGIN_DB,
    }

    for name, db in dbs.items():
        redis_clients[name] = redis.Redis(
            host=host, port=REDIS_PORT, db=db, encoding="utf-8", decode_responses=True
        )
        await redis_clients[name].ping()


async def close_redis():
    for client in redis_clients.values():
        await client.close()


def get_redis_db(db_name: str):

    async def get_client():
        client = redis_clients.get(db_name)
        if not client:
            raise Exception
        return client

    return get_client
