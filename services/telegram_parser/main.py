import datetime
import logging
import os

from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest, \
    GetFullChannelRequest
from telethon.types import MessageMediaPhoto, MessageMediaWebPage

from database.methods.main import Database
from database.models.media import MediaData
from database.models.posts import PostData
from database.models.channel import ChannelData
from services.cache.cache import Cache
from services.telegram_parser.add_posts import AddPosts
from settings.config import settings
from scheduler.main import scheduler

client = TelegramClient('9165797221',
                        settings.telegram_parser.api_id,
                        settings.telegram_parser.api_hash)


class TelegramParser:

    def __init__(self):
        self._db = Database()
        self._cli = client
        self._cache = Cache()

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

    async def _compare_posts(self, fresh_posts: list[PostData], posts_in_db: list[tuple]) -> list[PostData] | PostData:

        msg_id_old = [item[1] for item in posts_in_db]
        msg_id_new = [item.message_id for item in fresh_posts]

        diff = list(set(msg_id_old) ^ set(msg_id_new))

        return [p for p in fresh_posts if p.message_id in diff] if len(diff) > 1 else\
            [p for p in fresh_posts if p.message_id in diff][0]

    async def _get_type_entity(self, msg_data: dict, data: dict) -> PostData:
        if msg_data.get('media', None) is None:
            data['type'] = "text"
            return PostData.dict_to_post_data(data=data)
        elif msg_data['media']['_'] == "MessageMediaDocument":
            data['type'] = 'video'
            return PostData.dict_to_post_data(data=data)
        elif msg_data['media']['_'] == "MessageMediaPhoto":
            data['type'] = 'photo'

            photo_path = msg_data['media'].get('photo', None)
            if photo_path is not None:
                data['media'] = {
                    "type": "photo",
                    "post_id": msg_data['id'],
                    "file_name": "none",
                    "telegram_document_id": photo_path['id'],
                    "access_hash": photo_path['access_hash'],
                    "file_reference": str(photo_path['file_reference']),
                    "url": "none",
                    "web_id": 0,
                    "channel_id": msg_data['peer_id']['channel_id']
                }
            else:
                data['media'] = {}
            return PostData.dict_to_post_data(data=data)
        elif msg_data['media']['_'] == "MessageMediaWebPage":
            data['type'] = 'web_page'

            web_path = msg_data['media']['webpage']

            type_ = web_path['type']

            if type_ == "photo":
                photo_path = web_path.get('photo', None)

                if photo_path is not None:
                    data['media'] = {
                        "type": "web_page",
                        "post_id": msg_data['id'],
                        "file_name": "none",
                        "telegram_document_id": photo_path['id'],
                        "access_hash": photo_path['access_hash'],
                        "file_reference": str(photo_path['file_reference']),
                        "url": web_path['url'],
                        "web_id": web_path['id'],
                        "channel_id": msg_data['peer_id']['channel_id']
                    }
                else:
                    data['media'] = {}
            else:
                data['type'] = 'video'

            return PostData.dict_to_post_data(data=data)
        else:
            data['type'] = 'unknown'
            print(msg_data)
            return PostData.dict_to_post_data(data=data)

    async def _create_post_entity(self, message_data: dict) -> PostData:
        data = {
            "channel_id": message_data['peer_id']['channel_id'],
            "message_id": message_data.get('id', 0),
            "date": str(message_data.get('date', str(datetime.datetime.utcnow()))),
            "text": message_data['message'] if message_data.get('message', None) is not None else ""
        }
        return await self._get_type_entity(message_data, data)

    async def _download_media(self, media_entity: MessageMediaWebPage | MessageMediaPhoto, path: str):
        if isinstance(media_entity.media, MessageMediaPhoto):
            filepath = path + f"/{media_entity.media.photo.id}.jpg"
            if os.path.exists(filepath):

                return "none"
            else:
                await self._cli.download_media(media_entity.media, path + f"/{media_entity.media.photo.id}.jpg")

                return filepath
        elif isinstance(media_entity.media, MessageMediaWebPage):
            filepath = path + f"/{media_entity.media.webpage.photo.id}.jpg"
            if os.path.exists(filepath):

                return "none"
            else:
                await self._cli.download_media(media_entity.media,
                                               path + f"/{media_entity.media.webpage.photo.id}.jpg")
                return filepath
        else:
            print("UNKNOWN TYPE")

    async def _save_photo(self, photo_entity) -> str:
        root_path = settings.project_const.root
        today_folder = f'{root_path}/static/{datetime.datetime.date(datetime.datetime.utcnow())}'

        if os.path.exists(today_folder):
            return await self._download_media(photo_entity, today_folder)
        else:
            os.mkdir(today_folder)
            return await self._download_media(photo_entity, today_folder)

    async def _create_media(self, media: PostData, photo_path: str) -> MediaData:
        return MediaData.post_data_to_media_data(media, photo_path=photo_path)

    async def _get_limited_messages(self, entity, limit=settings.telegram_parser.max_update_post):

        list_post_data = []
        media_data = []

        async for msg in self._cli.iter_messages(entity=entity, limit=limit):

            try:
                post_ = await self._create_post_entity(message_data=msg.to_dict())

                if post_.type != "video" and post_.text != "" and len(post_.text) > 100:
                    if post_.type == "photo" or post_.type == "web_page":

                        photo_path = await self._save_photo(photo_entity=msg)
                        print("photo path in telegram_parser -> _get_limited_msg -> photo_path ", photo_path)
                        media_data.append(await self._create_media(post_, photo_path=photo_path))

                    list_post_data.append(post_)

            except Exception as e:
                logging.info(f"Error in get_limited_message: {e}")
                continue

        if media_data:
            add_post = AddPosts(new_post=list_post_data, media=media_data)
        else:
            add_post = AddPosts(new_post=list_post_data)

        await add_post.init_add_new_posts()

    async def get_full_channel_info(self, entity=None, link=None):
        if entity is not None:
            return await self._cli(GetFullChannelRequest(channel=entity))
        else:
            entity_ = await self._cli.get_entity(entity=link)
            return await self._cli(GetFullChannelRequest(channel=entity_))

    async def start_parsing(self):

        channels_data = await self._db.get_channels()

        if channels_data:
            for channel in channels_data:
                try:
                    entity = await self._cli.get_entity(entity=channel.link)
                    entity_to_dict = entity.to_dict()

                    if entity_to_dict['_'] == "Channel":
                        channel_info = await self.get_full_channel_info(entity=entity)
                        await self._join_to_channel(entity=entity, channel=channel, channel_info=channel_info.to_dict())

                        await self._get_limited_messages(entity=entity)

                except Exception as e:
                    logging.info(e)
        else:
            print("We not find channels for parsing")
