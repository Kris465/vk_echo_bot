import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
from loguru import logger
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")

# Настройка логирование
logger.add("bot.log", rotation="1 MB", retention="7 days", level="INFO")
logger.info("Бот запускается...")


def main():
    vk_session = vk_api.VkApi(token=TOKEN)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    logger.info("Бот запущен. Ожидаю сообщения...")

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            user_id = event.user_id
            message_text = event.text

            logger.info(f"Сообщение от {user_id}: {message_text}")

            if message_text.lower() in ("привет", "hello", "hi", "здравствуйте"):
                greeting = "Привет! Я эхо-бот. Напиши мне что-нибудь, и я повторю."
                vk.messages.send(
                    user_id=user_id,
                    message=greeting,
                    random_id=0,
                )
                logger.info(f"Отправлено приветствие для {user_id}")
            else:
                vk.messages.send(
                    user_id=user_id,
                    message=message_text,
                    random_id=0,
                )


if __name__ == "__main__":
    main()
