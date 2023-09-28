from database.methods.main import Database
from database.models.posts import PostData
from settings.config import settings
from database.models.modify_post import ModifyPostData, ModifyPost
import openai


class OpenAiApi:
    _client = openai
    _client.organization = settings.open_ai.open_ai_organization
    _client.api_key = settings.open_ai.open_ai_token

    def __init__(self):
        self.database = Database()

    async def run_job(self, data: PostData) -> None:

        new_text = await self._send_request(text=data['text'])
        new_text += f"\n\n<a href='{settings.project_const.main_url}'>" \
                    f"{settings.project_const.title}</a>"

        update_data = {
            "state": "await",
        }

        await self.database.update_post(post_id=data['id'], data=update_data)
        mod_text_entity = ModifyPostData(post_id=data['message_id'],
                                         text=new_text,
                                         channel_id=data['channel_id'],
                                         type=data['type'])

        await self.database.add_any_item(item=ModifyPost(mod_text_entity))

    async def _create_message(self, text):
        return f"{settings.project_const.default_prompt} {text}"

    async def _send_request(self, text: str):
        try:
            r = self._client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": f"{await self._create_message(text=text)}"}
                ]
            )
            return r.choices[0].message['content']
        except Exception as e:
            print(e)
            return "Ошибка при отправке запроса."
