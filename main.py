import asyncio
from aiogram import Bot, Dispatcher

from config import load_config
from handlers import base_handler, find_handler, load_handler
from repository import Repository


async def main():
    config = load_config()
    bot = Bot(token=config.bot.token)
    repo = Repository()
    repo.tgbot = bot
    repo.config = config
    dp = Dispatcher()

    dp.include_router(base_handler.router)
    dp.include_router(find_handler.router)
    dp.include_router(load_handler.router)

    await repo.tgbot.delete_webhook(drop_pending_updates=True)

    print("Инициализация прошла успешно!")
    await dp.start_polling(repo.tgbot)


if __name__ == '__main__':
    asyncio.run(main())
