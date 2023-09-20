from database.methods.main import Database
from database.models.media import MediaData, Media
from database.models.posts import PostData, Post
from services.cache.cache import Cache
from scheduler.main import scheduler
from settings.config import settings


class AddPosts:

    def __init__(self, new_post: list[PostData] = None, media: list[MediaData] = None):
        self._db = Database()
        self._cache = Cache()
        self.last_posts = new_post
        self.media = media

    async def _add_new_posts(self, posts: list[PostData] = None, media: list[MediaData] = None) -> None | str:

        if posts is not None:
            to_post = [Post(post) for post in posts]
            scheduler.add_job(func=self._db.add_posts, kwargs={"items": to_post})
        elif media is not None:
            to_media = [Media(m) for m in media]
            scheduler.add_job(func=self._db.add_posts, kwargs={"items": to_media})
        else:
            return 'ERROR'

    async def _compare_posts(self, fresh_posts: list[PostData], posts_in_db: list[tuple]) -> list[PostData]:

        msg_id_old = [item[1] for item in posts_in_db]
        msg_id_new = [item.message_id for item in fresh_posts]

        diff = list(set(msg_id_old) ^ set(msg_id_new))

        return [p for p in fresh_posts if p.message_id in diff]

    async def init_add_new_posts(self) -> None:
        channel_id = self.last_posts[0].channel_id

        posts = [(item.id, item.message_id) for item in
                 await self._db.get_posts_for_compare_(channel_id=channel_id)]

        if posts:
            post_not_in_database = await self._compare_posts(fresh_posts=self.last_posts,
                                                             posts_in_db=posts[-settings.telegram_parser.max_update_post:])

            if post_not_in_database:
                await self._add_new_posts(posts=post_not_in_database)

        else:
            await self._add_new_posts(posts=self.last_posts[::-1])

            if self.media is not None:
                await self._add_new_posts(media=self.media)
