import asyncio
from aiogram import Bot, Dispatcher

from config import Config, load_config
from handlers import base_handler, find_handler


async def main():
    config = load_config()
    bot = Bot(token=config.bot.token)
    dp = Dispatcher()

    dp.include_router(base_handler.router)
    dp.include_router(find_handler.router)

    await bot.delete_webhook(drop_pending_updates=True)

    print("Инициализация прошла успешно!")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
