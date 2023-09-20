from database.methods.main import Database
from redis_.main import RedisClient


class Cache:

    def __init__(self):
        self.redis_cli = RedisClient()
        self.db = Database()

    async def get_all_post_id(self, channel_id: int):

        result = await self.redis_cli.get_all_messages_id(channel_id=channel_id)

        if result:
            return result
        else:
            posts = await self.db.get_all_post_id_by_channel_id(channel_id=channel_id)
            await self.redis_cli.set_all_messages_id(channel_id=channel_id, data=posts)

    async def update_all_post_id(self, channel_id: int, data: list[int]):
        await self.redis_cli.clean_obj(key=f"messages_id:{channel_id}")
        await self.redis_cli.set_all_messages_id(channel_id=channel_id,
                                                 data=data)

        return self.get_all_post_id(channel_id=channel_id)

    async def get_user(self, user_id: int):
        ...
