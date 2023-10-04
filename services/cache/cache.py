from database.methods.main import Database
from database.models.user import UserData
from database.models.posts import PostData
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
            self._redis_cli.set_cache_user_by_id(user_id=user_id, data=user.to_dict())

            user = await self._redis_cli.get_cache_user_by_id(user_id=user_id)

            return UserData(id=user['id'],
                            active_msg_id=user['active_msg_id'],
                            name=user['name'],
                            phone=user['phone'],
                            is_admin=(False, True)[user['is_admin'] == "1"],
                            update_at=user['update_at'],
                            email=user['email'])

    async def _set_user_data(self, user: UserData):
        self._redis_cli.set_cache_user_by_id(user_id=user.id, data=user.to_dict())
        return await self.get_user(user_id=user.id)

    async def update_user(self, user: UserData):
        await self._database.update_user(user_id=user.id, update_data=user.to_dict())
        return await self._set_user_data(user=user)

    async def get_admins(self) -> list[UserData] | list:
        result_data = []
        admins = self._redis_cli.get_all_admins_id()

        if admins:
            for admin_id in admins:
                admin_data = await self.get_user(user_id=admin_id)
                result_data.append(admin_data)
        else:
            admins = await self._database.get_all_admin_with_main_admin()
            for admin_id in admins:
                self._redis_cli.set_all_admins_id(data=admin_id)
                result_data.append(await self.get_user(user_id=admin_id))

        return result_data

    async def update_state_admins(self):
        self._redis_cli.clean_obj(key='admins')
        admins = await self._database.get_all_admin_with_main_admin()
        for admin_id in admins:
            self._redis_cli.set_all_admins_id(data=admin_id)

    async def get_post(self, message_id: int, channel_id: int):
        post = self._redis_cli.get_post_(message_id=message_id, channel_id=channel_id)

        if post:
            for k, v in post.items():
                if k == 'reject':
                    post[k] = (False, True)[v == '1']
                elif k == 'published':
                    post[k] = (False, True)[v == '1']
                elif k == 'media':
                    post[k] = {}
                else:
                    pass

            return PostData.dict_to_post_data(data=post)
        else:
            post = await self._database.get_post_(message_id=message_id, channel_id=channel_id)
            self._redis_cli.set_post_(message_id=message_id, channel_id=channel_id, data=post[0].to_dict())

            return await self.get_post(message_id=message_id, channel_id=channel_id)
