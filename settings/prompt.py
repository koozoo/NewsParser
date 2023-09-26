from database.methods.main import Database
from database.models.openai import OpenaiData, Openai
from settings.config import settings


async def prompt() -> None:
    database = Database()

    dp = await database.get_prompt_()

    if dp:
        settings.project_const.default_prompt = dp[0].prompt
    else:
        prompt_data = {
            "prompt": "Вам будет дана статья или сообщение для переработки. Ваша цель - "
                      "переписать содержание, сохраняя"
                      "ясность и краткость, сохраняя при этом оригинальный смысл. Ваш "
                      "переписанный контент должен быть"
                      f"увлекательным и легким для чтения. Так же необходимо,"
                      f" очистить текст от всех слов содержащих знаки # и @. Вот статья:",
            "type": "Default"
        }

        dtt = OpenaiData(prompt=prompt_data['prompt'], type=prompt_data['type'])
        await database.add_any_item(item=Openai(dtt))

        settings.project_const.default_prompt = prompt_data['prompt']
