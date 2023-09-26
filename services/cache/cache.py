from database.methods.main import Database
from database.models.user import UserData
from redis_.main import RedisClient


class Cache:

    def __init__(self):
        self._redis_cli = RedisClient()
        self._database = Database()

    async def get_user(self, user_id: int):

        user = await self._redis_cli.get_cache_user_by_id(user_id=user_id)
        if user:
            return UserData(id=user['id'],
                            active_msg_id=user['active_msg_id'],
                            name=user['name'],
                            phone=user['phone'],
                            is_admin=(False, True)[user['is_admin'] == "1"],
                            update_at=user['update_at'],
                            email=user['email'])
        else:
            user = await self._database.get_user(user_id=user_id)
            await self._redis_cli.set_cache_user_by_id(user_id=user_id, data=user.to_dict())

            user = await self._redis_cli.get_cache_user_by_id(user_id=user_id)

            return UserData(id=user['id'],
                            active_msg_id=user['active_msg_id'],
                            name=user['name'],
                            phone=user['phone'],
                            is_admin=(False, True)[user['is_admin'] == "1"],
                            update_at=user['update_at'],
                            email=user['email'])

    async def _set_user_data(self, user: UserData):
        await self._redis_cli.set_cache_user_by_id(user_id=user.id, data=user.to_dict())
        return await self.get_user(user_id=user.id)

    async def update_user(self, user: UserData):
        await self._database.update_user(user_id=user.id, update_data=user.to_dict())
        return await self._set_user_data(user=user)

