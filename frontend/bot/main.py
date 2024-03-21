import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties

from config import BOT_TOKEN
from handlers import commands, callbacks, work_space

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))


async def main():
    dp = Dispatcher()
    dp.include_routers(commands.router, callbacks.router, work_space.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
