import datetime
import logging

from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest, \
    GetFullChannelRequest

from database.methods.main import Database
from database.models.posts import Post, PostData
from database.models.channel import ChannelData
from settings.config import settings
from scheduler.main import scheduler

client = TelegramClient('9165798836',
                        settings.telegram_parser.api_id,
                        settings.telegram_parser.api_hash)


class TelegramParser:

    def __init__(self):
        self._db = Database()
        self._cli = client

    async def _join_to_channel(self, entity, channel: ChannelData, channel_info: dict):
        channel_data = entity.to_dict()

        channel.telegram_channel_id = channel_info['full_chat']['id']
        channel.description = channel_info['full_chat']['about']
        channel.name = channel_data['title']

        if channel_data['left'] is True:
            await self._cli(JoinChannelRequest(channel=entity))

            update_channel_data = {
                "name": channel.name,
                "description": channel.description,
                "telegram_channel_id": channel.telegram_channel_id
            }

            scheduler.add_job(func=self._db.update_channel, kwargs={"channel_id": channel.id,
                                                                    "channel_data": update_channel_data})

    async def _compare_posts(self, new_posts: list[PostData], old_posts: list[tuple]) -> list:
        result = []

        index_for_update = [index[0] for index in old_posts]

        msg_id_old = [item[1] for item in old_posts]
        msg_id_new = [item.message_id for item in new_posts]

        diff = list(set(msg_id_old) ^ set(msg_id_new))

        if diff:

            for item in new_posts:

                if item.message_id in diff:
                    try:
                        get_index = index_for_update.index(max(index_for_update))
                        index = index_for_update.pop(get_index)
                        item.id = index
                        item.state = "new"
                        result.append({
                            index: item
                        })
                    except Exception as e:
                        logging.info(e)
                        break

        return result

    async def _update_last_messages(self, last_posts: list[PostData]):
        new_posts = []

        channel_id = last_posts[0].channel_id

        posts = [(item.id, item.message_id, item.state) for item in
                 await self._db.get_posts_by_channel_id(channel_id=channel_id)]

        if posts:

            new_posts = await self._compare_posts(new_posts=last_posts,
                                                  old_posts=posts)

            if len(posts) + len(new_posts) < settings.telegram_parser.max_update_post:
                new_items = []

                for i in new_posts:
                    for k, v in i.items():
                        new_items.append(v)

                await self._db.add_posts(items=[Post(item) for item in new_items])
                logging.info(await self._cache.update_last_msg(channel_id=channel_id))
            else:

                await self._db.update_posts(items=new_posts)
                logging.info(await self._cache.update_last_msg(channel_id=channel_id))

        else:
            await self._db.add_posts(items=[Post(item) for item in last_posts])

        all_id = [post[0] for post in posts]

        if new_posts:
            for new_post in new_posts:
                for id_ in new_post.keys():
                    if id_ in all_id:
                        idx = all_id.index(id_)
                        all_id.pop(idx)

            await self._update_status_post(all_id=all_id, posts=posts)
        else:
            await self._update_status_post(all_id=all_id, posts=posts)

    async def _update_status_post(self, all_id, posts):

        for post in posts:
            if post[0] in all_id and post[2] != "old":
                await self._db.update_post(post_id=post[0], data={"state": "old"})

    async def _get_type(self, msg_data: dict, data: dict) -> str:

        if msg_data.get('media', None) is None:
            data['type'] = "text"
            return PostData.dict_to_post_data(data=data)
        elif msg_data['media']['_'] == "MessageMediaDocument":
            data['type'] = 'video'
            return PostData.dict_to_post_data(data=data)
        elif msg_data['media']['_'] == "MessageMediaPhoto":
            data['type'] = 'photo'
            return PostData.dict_to_post_data(data=data)
        elif msg_data['media']['_'] == "MessageMediaWebPage":
            data['type'] = 'web_page'
            return PostData.dict_to_post_data(data=data)
        else:
            return PostData.dict_to_post_data(data=data)

    async def _create_post_entity(self, message_data: dict):
        data = {
            "channel_id": message_data['peer_id']['channel_id'],
            "message_id": message_data.get('id', 0),
            "date": str(message_data.get('date', str(datetime.datetime.utcnow()))),
            "text": message_data['message'] if message_data.get('message', None) is not None else ""
        }
        return await self._get_type(message_data, data)

    async def _get_limited_messages(self, entity, limit=settings.telegram_parser.max_update_post):

        list_post_data = []

        async for msg in self._cli.iter_messages(entity=entity, limit=limit):
            try:
                list_post_data.append(await self._create_post_entity(message_data=msg.to_dict()))
            except Exception as e:
                logging.info(f"Error in get_limited_message: {e}")
                continue
        print(list_post_data)
        #
        # await self._update_last_messages(last_posts=list_post_data)
        #
        # return list_post_data

    async def _get_full_channel_info(self, entity):
        return await self._cli(GetFullChannelRequest(channel=entity))

    async def start_parsing(self):

        channels_data = await self._db.get_channels()

        if channels_data:
            for channel in channels_data:
                try:
                    entity = await self._cli.get_entity(entity=channel.link)
                    entity_to_dict = entity.to_dict()

                    if entity_to_dict['_'] == "Channel":
                        channel_info = await self._get_full_channel_info(entity=entity)
                        await self._join_to_channel(entity=entity, channel=channel, channel_info=channel_info.to_dict())

                        await self._get_limited_messages(entity=entity)

                except Exception as e:
                    logging.info(e)
        else:
            print("not data")
