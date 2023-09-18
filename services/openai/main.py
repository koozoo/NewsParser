from database.models.posts import PostData
from services.openai.api import OpenAiApi


class OpenAi:

    def __init__(self, posts: list[PostData]):
        self.posts = posts
        self._api = OpenAiApi()

    async def init_job(self):
        await self._run_manager()

    async def _run_manager(self):
        print("manager posts ", self.posts)
        while self.posts:

            job = self.posts.pop()
            print(job)
            return await self._api.run_job(job)

