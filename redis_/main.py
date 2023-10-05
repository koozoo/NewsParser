import datetime

import redis
import settings as config


class RedisClient:

    _default_expire: 2400

    def __init__(self, db: int = 0):

        self.host = config.settings.redis.host
        self.port = config.settings.redis.port
        self.db = db
        self.password = config.settings.redis.pass_
        self.socket_timeout = None

    def _connect_redis(self):
        if self.password is not None:

            return redis.Redis(host=self.host,
                               port=self.port,
                               db=self.db,
                               password=self.password,
                               decode_responses=True)

        else:
            print("redis is None")
            return redis.Redis(host=self.host,
                               port=self.port,
                               db=self.db,
                               decode_responses=True)

    def set_all_messages_id(self, channel_id: int,  data: list[int]):
        with self._connect_redis() as redis_cli:
            for post in data:
                redis_cli.rpush(f"messages_id:{channel_id}", post)
                redis_cli.expire(f"messages_id:{channel_id}", 2400)

    def get_all_messages_id(self, channel_id: int):
        with self._connect_redis() as redis_cli:
            data = redis_cli.lrange(f"messages_id:{channel_id}", 0, -1)
            return data

    def clean_obj(self, key: str):
        with self._connect_redis() as redis_cli:
            redis_cli.delete(key)

    async def get_cache_user_by_id(self, user_id: int):
        with self._connect_redis() as redis_cli:
            return redis_cli.hgetall(f"user:{user_id}")

    def set_cache_user_by_id(self, user_id: int, data: dict):
        with self._connect_redis() as redis_cli:

            for key, value in data.items():

                if value is True:
                    value = 1
                elif value is False:
                    value = 0
                elif isinstance(value, datetime.datetime):
                    value = str(value)
                else:
                    pass

                redis_cli.hset(f"user:{user_id}", key=key, value=value)
                redis_cli.expire(f"user:{user_id}", 2400)

    def get_all_admins_id(self):
        with self._connect_redis() as redis_cli:
            return redis_cli.lrange(f"admins", 0, -1)

    def set_all_admins_id(self, data):
        with self._connect_redis() as redis_cli:
            redis_cli.rpush(f"admins", data)

    def set_post_(self, message_id: int, channel_id: int, data: dict):
        with self._connect_redis() as redis_cli:

            for k, v in data.items():
                if v is True:
                    v = 1
                elif v is False:
                    v = 0
                elif isinstance(v, datetime.datetime):
                    v = str(v)
                elif v is None:
                    v = 'none'
                else:
                    pass

                redis_cli.hset(f"post:{message_id}:{channel_id}", key=k, value=v)
                redis_cli.expire(f"post:{message_id}:{channel_id}", 2400)

    def get_post_(self, message_id: int, channel_id: int):
        with self._connect_redis() as redis_cli:
            return redis_cli.hgetall(f"post:{message_id}:{channel_id}")
