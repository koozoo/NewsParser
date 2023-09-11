# import datetime
# import logging
# 
# from telethon.tl.functions.channels import JoinChannelRequest, \
#     GetFullChannelRequest
# from telethon.tl.types import PeerChat, PeerUser, PeerChannel, \
#     Message as TelethonMessage, User as TelethonUser, \
#     Channel as ChannelTelethon, Chat
# 
# from bot.configs.settings import MAX_UPDATE_MESSAGES
# from bot.database.methods.main import Database
# from bot.clients import client
# from bot.database.models.posts import Post, PostData
# from bot.database.models.user import UserData, User
# from bot.database.models.user_channel import UserChannel, UserChannelData
# from bot.parser_data.utils import convert_dict_to_task_item, convert_dict_to_channel_data
# from bot.database.models.channel import Channel, ChannelData
# from bot.service.cache import Cache
# 
# 
class TelegramParser:

    def __init__(self, uid: int, task_data: dict):
        self.task_data = task_data
# 
#     async def _join(self, entity):
#         return await self._cli(JoinChannelRequest(channel=entity))
# 
#     async def _get_type_entity(self, entity):
# 
#         if isinstance(entity, PeerChannel):
#             return "PeerChannel"
#         elif isinstance(entity, PeerChat):
#             return "PeerChat"
#         elif isinstance(entity, ChannelTelethon):
#             return "Channel"
#         elif isinstance(entity, Chat):
#             return "Chat"
#         elif isinstance(entity, TelethonMessage):
#             return 'Message'
#         elif isinstance(entity, TelethonUser):
#             return 'User'
#         elif isinstance(entity, PeerUser):
#             return "PeerUser"
#         else:
#             return "Unexpected type"
# 
#     async def _check_channel_in_db(self, channel_id: int) -> bool:
#         return any([item.id for item in
#                     await self._db.get_channel(channel_id=channel_id)])
# 
#     async def _concat_full_name(self, f_name: str, l_name: str) -> str:
# 
#         if f_name is not None:
#             pass
#         else:
#             f_name = ''
# 
#         if l_name is not None:
#             pass
#         else:
#             l_name = ''
# 
#         if f_name and l_name:
#             return f_name + " " + l_name
#         elif f_name:
#             return f_name
#         elif l_name:
#             return l_name
#         else:
#             return "Noname"
# 
#     async def _cast_to_user_data(self, user: dict):
# 
#         u_data = UserData(
#             id=int(user['id']),
#             role=1,
#             full_name=str(await self._concat_full_name(f_name=user['first_name'], l_name=user['last_name'])),
#             user_name=str(user['username'])
#         )
# 
#         return u_data
# 
#     async def create_users_in_db(self, users: dict, channel_id: int):
#         user_list = []
#         user_for_user_channel = []
# 
#         # CHECK USER IN DB
#         users_in_db = {
#             item.id: UserData(
#                 id=item.id,
#                 role=item.role,
#                 full_name=item.full_name,
#                 user_name=item.user_name,
#                 phone=item.phone,
#                 email=item.email,
#                 is_subscribed=item.is_subscribed
#             ) for item in await self._db.get_all_users()
#         }
# 
#         # CHECK USER IN USER_CHANNEL
#         all_users_in_group = {
#             item.user_id: UserData(
#                 id=item.id,
#                 channel_id=item.channel_id,
#                 user_id=item.user_id
#             ) for item in
#             await self._db.get_all_users_in_channel(cid=channel_id)
#         }
# 
#         for user in users['all_users']:
#             if user['id'] in users_in_db:
#                 if user['id'] in all_users_in_group:
#                     continue
#                 else:
#                     user_for_user_channel.append(await self._cast_to_user_data(user=user))
#                 continue
#             else:
#                 user_list.append(User(await self._cast_to_user_data(user=user)))
#                 user_for_user_channel.append(await self._cast_to_user_data(user=user))
# 
#         if user_list:
#             await self._db.add_users(users=user_list)
# 
#         if user_for_user_channel:
#             await self._create_userchannel_in_db(users=user_for_user_channel,
#                                                  channel_id=channel_id)
# 
#         return user_for_user_channel
# 
#     async def _create_userchannel_in_db(self, users: list[UserData],
#                                         channel_id: int):
# 
#         user_channel_list = []
# 
#         for user in users:
#             user_channel = UserChannelData(
#                 user_id=user.id,
#                 channel_id=channel_id
#             )
# 
#             user_channel_list.append(UserChannel(user_channel))
# 
#         await self._db.add_user_channel(items=user_channel_list)
# 
#     async def _compare_posts(self, new_posts: list[PostData], old_posts: list[tuple]) -> list:
#         result = []
# 
#         index_for_update = [index[0] for index in old_posts]
# 
#         msg_id_old = [item[1] for item in old_posts]
#         msg_id_new = [item.message_id for item in new_posts]
# 
#         diff = list(set(msg_id_old) ^ set(msg_id_new))
# 
#         if diff:
# 
#             for item in new_posts:
# 
#                 if item.message_id in diff:
#                     try:
#                         get_index = index_for_update.index(max(index_for_update))
#                         index = index_for_update.pop(get_index)
#                         item.id = index
#                         item.state = "new"
#                         result.append({
#                             index: item
#                         })
#                     except Exception as e:
#                         logging.info(e)
#                         break
# 
#         return result
# 
#     async def _update_last_messages(self, last_posts: list[PostData]):
#         new_posts = []
# 
#         channel_id = last_posts[0].channel_id
# 
#         posts = [(item.id, item.message_id, item.state) for item in
#                  await self._db.get_posts_by_channel_id(channel_id=channel_id)]
# 
#         if posts:
# 
#             new_posts = await self._compare_posts(new_posts=last_posts,
#                                                   old_posts=posts)
# 
#             if len(posts) + len(new_posts) < MAX_UPDATE_MESSAGES:
#                 new_items = []
# 
#                 for i in new_posts:
#                     for k, v in i.items():
#                         new_items.append(v)
# 
#                 await self._db.add_posts(items=[Post(item) for item in new_items])
#                 logging.info(await self._cache.update_last_msg(channel_id=channel_id))
#             else:
# 
#                 await self._db.update_posts(items=new_posts)
#                 logging.info(await self._cache.update_last_msg(channel_id=channel_id))
# 
#         else:
#             await self._db.add_posts(items=[Post(item) for item in last_posts])
# 
#         all_id = [post[0] for post in posts]
# 
#         if new_posts:
#             for new_post in new_posts:
#                 for id_ in new_post.keys():
#                     if id_ in all_id:
#                         idx = all_id.index(id_)
#                         all_id.pop(idx)
# 
#             await self._update_status_post(all_id=all_id, posts=posts)
#         else:
#             await self._update_status_post(all_id=all_id, posts=posts)
# 
#     async def _update_status_post(self, all_id, posts):
# 
#         for post in posts:
#             if post[0] in all_id and post[2] != "old":
#                 await self._db.update_post(post_id=post[0], data={"state": "old"})
# 
#     async def _create_chanel_in_db(self, chanel: ChannelData):
#         channel = Channel(chanel)
#         new_chanel_data = await self._db.add_channel(channel_data=chanel, channel=channel)
# 
#         return new_chanel_data
# 
#     async def _create_post_entity(self, message_data: dict):
# 
#         all_reactions_count = 0
#         reactions = message_data.get('reactions', None)
#         if reactions is not None:
#             reactions_data = reactions.get('results', None)
#             if reactions_data:
#                 for reaction_item in reactions_data:
#                     if reaction_item is not None:
#                         all_reactions_count += reaction_item['count']
#                     else:
#                         continue
# 
#         replies = message_data.get('replies', None)
#         if replies is not None:
#             replies_cid = replies.get('channel_id', 0)
#             if replies_cid is None:
#                 replies_cid = 0
#         else:
#             replies_cid = 0
# 
#         message_id = message_data.get('id', 0)
#         date = str(message_data.get('date', str(datetime.datetime.utcnow())))
# 
#         text = message_data.get('message', '')
#         if text is None:
#             text = ''
# 
#         views_count = message_data.get('views', 0)
#         if views_count is None:
#             views_count = 0
# 
#         channel_id = message_data['peer_id']['channel_id']
# 
#         if text:
#             return PostData(channel_id=channel_id,
#                             message_id=message_id,
#                             date=date,
#                             text=text,
#                             state="new",
#                             views_count=views_count,
#                             reactions_count=all_reactions_count,
#                             comments_channel_id=replies_cid)
#         else:
#             return PostData(channel_id=channel_id,
#                             message_id=message_id,
#                             date=date,
#                             text=text,
#                             state="new",
#                             views_count=views_count,
#                             reactions_count=all_reactions_count,
#                             comments_channel_id=replies_cid,
#                             type="Media/Docs")
# 
#     async def _get_limited_messages(self, entity, limit=10):
# 
#         list_post_data = []
# 
#         async for msg in self._cli.iter_messages(entity=entity, limit=limit):
#             try:
#                 list_post_data.append(await self._create_post_entity(message_data=msg.to_dict()))
#             except Exception as e:
#                 logging.info(f"Error in get_limited_message: {e}")
#                 continue
# 
#         await self._update_last_messages(last_posts=list_post_data)
# 
#         return list_post_data
# 
#     async def _get_full_channel_info(self, entity):
#         channel_info = await self._cli(GetFullChannelRequest(channel=entity))
#         return channel_info
# 
#     async def _add_unique_users(self, entity, channel_id: int):
#         all_users_in_channel = await self._get_users(entity=entity)
#         if all_users_in_channel is not None:
#             user_data_list = await self.create_users_in_db(users=all_users_in_channel, channel_id=channel_id)
# 
#             return user_data_list
#         else:
#             return None
# 
#     async def _compare_subscribers(self, entity):
#         channel_info = await self._get_full_channel_info(entity=entity)
#         full_info = channel_info.to_dict()
#         last_total_users_in_chanel = [item.user_count for item in await self._db.get_channel(
#             channel_id=full_info['full_chat']['id'])]
#         user_count = full_info['full_chat']['participants_count']
# 
#         return f"Новых подписчиков: {user_count - last_total_users_in_chanel[0]}"
# 
#     async def _get_users(self, entity) -> None | dict:
# 
#         try:
#             result = {"all_users": None}
#             tmp = []
#             async for user in client.iter_participants(entity=entity, aggressive=True):
#                 tmp.append(user.to_dict())
#             result['all_users'] = tmp
# 
#             return result
# 
#         except Exception as e:
#             print(f"Undefined exception: {e}")
# 
#             return None
# 
#     async def start_parsing(self):
# 
#         task = await convert_dict_to_task_item(task_item=self.task_data)
# 
#         try:
#             entity = await self._cli.get_entity(task.target_url)
#             entity_to_dict = entity.to_dict()
#             entity_type = await self._get_type_entity(entity=entity)
#             task.channel_id = entity_to_dict['id']
# 
#             if entity_type == "Channel":
#                 if entity_to_dict['left'] is True:
#                     await self._join(entity)
#                 if not await self._check_channel_in_db(channel_id=entity_to_dict['id']):
#                     channel_info = await self._get_full_channel_info(entity=entity)
#                     full_channel_info = channel_info.to_dict()
#                     channel = await convert_dict_to_channel_data(link=task.target_url,
#                                                                  entity_data=entity_to_dict,
#                                                                  channel_info=full_channel_info)
# 
#                     await self._create_chanel_in_db(chanel=channel)
# 
#                     await self._add_unique_users(entity=entity, channel_id=entity_to_dict['id'])
# 
#                     print(await self._get_limited_messages(entity=entity))
#                 else:
#                     print(await self._get_limited_messages(entity=entity))
#                     await self._add_unique_users(entity=entity, channel_id=entity_to_dict['id'])
# 
#             # CHANGE STATUS
#             task_item_update = {
#                 "channel_id": task.channel_id,
#                 "status": "success"
#             }
# 
#             await self._db.update_task_item(task_item_id=task.id, update_data=task_item_update)
# 
#         except Exception as e:
#             logging.info(e)
# 
#             task_item_update = {
#                 "status": "error"
#             }
# 
#             await self._db.update_task_item(task_item_id=task.id, update_data=task_item_update)
