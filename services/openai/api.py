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

        update_data = {
            "state": "await",
        }

        await self.database.update_post(post_id=data['id'], data=update_data)

        mod_text_entity = ModifyPostData(post_id=data['id'],
                                         text=new_text)

        await self.database.add_any_item(item=ModifyPost(mod_text_entity))

    async def _create_message(self, text):
        return ("Вам будет дана статья или сообщение для переработки. Ваша цель - переписать содержание, сохраняя "
                "ясность и краткость, сохраняя при этом оригинальный смысл. Ваш переписанный контент должен быть "
                f"увлекательным и легким для чтения. Так же необходимо,"
                f" очистить тест от всех слов содержащих знаки # и @. Вот статья: {text}")

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
