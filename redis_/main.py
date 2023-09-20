import redis
import settings as config


class RedisClient:

    def __init__(self, db: int = 0):

        self.host = config.settings.redis.host
        self.port = config.settings.redis.port
        self.db = db
        self.password = config.settings.redis.pass_
        self.socket_timeout = None

    def _connect_redis(self):
        if self.password:
            return redis.Redis(host=self.host,
                               port=self.port,
                               db=self.db,
                               password=self.password,
                               decode_responses=True)

        else:
            return redis.Redis(host=self.host,
                               port=self.port,
                               db=self.db,
                               decode_responses=True)

    async def set_all_messages_id(self, channel_id: int,  data: list[int]):
        with self._connect_redis() as redis_cli:
            for post in data:
                await redis_cli.rpush(f"messages_id:{channel_id}", post)

    async def get_all_messages_id(self, channel_id: int):
        with self._connect_redis() as redis_cli:
            data = redis_cli.lrange(f"messages_id:{channel_id}", 0, -1)
            return data

    async def clean_obj(self, key: str):
        with self._connect_redis() as redis_cli:
            await redis_cli.delete(key)

    async def get_cache_user_by_id(self, user_id: int):
        with self._connect_redis() as redis_cli:
            await redis_cli.hgetall(f"user:{user_id}")

    async def set_cache_user_by_id(self, user_id: int, data: dict):
        with self._connect_redis() as redis_cli:
            for key, value in data.items():

                await redis_cli.hset(f"user:{user_id}", key=key, value=value)
