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

    async def create_listener_api_task(self):
        with self._connect_redis() as redis_cli:
            listener = redis_cli.pubsub()
            listener.subscribe("new_job_for::bot")

            return listener

    async def set_cache_all_user_by_channel_id(self, channel_id: int, data: str):
        with self._connect_redis() as redis_cli:

            await redis_cli.set(f"userchannel:{channel_id}", data)

        return await self.get_cache_all_user_by_channel_id(channel_id=channel_id)

    async def get_cache_all_user_by_channel_id(self, channel_id: int):
        with self._connect_redis() as redis_cli:
            data = redis_cli.get(f"userchannel:{channel_id}")
            return data

    async def set_last_messages(self, channel_id: int, data: str):
        with self._connect_redis() as redis_cli:
            await redis_cli.set(f"messages:{channel_id}", data)

    async def get_last_messages(self, channel_id: int):
        with self._connect_redis() as redis_cli:
            data = redis_cli.get(f"messages:{channel_id}")
            return data

    async def clean_obj(self, key: str, **kwargs):
        with self._connect_redis() as redis_cli:
            redis_cli.delete(key)

            if kwargs:
                redis_cli.set(key, kwargs['data'])
