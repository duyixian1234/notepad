import os

from redis import Redis


async def get_redis():
    yield Redis(
        host=os.getenv("REDIS_URL"),
        port=37513,
        password=os.getenv("REDIS_PASSWORD"),
        ssl=True,
    )
