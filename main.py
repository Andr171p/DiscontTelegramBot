import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from telegram.config import BotToken
from telegram.bot.handlers.start import start_router
from telegram.bot.handlers.register import register_router
from telegram.bot.handlers.status import status_router

from broadcast.send import Broadcast


bot = Bot(token=BotToken().token, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
dp.include_routers(
    start_router,
    register_router,
    status_router
)


async def broadcast() -> None:
    broadcaster = Broadcast(bot=bot)
    await broadcaster.broadcast()


async def telegram() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


async def main() -> None:
    await asyncio.gather(
        broadcast(),
        telegram()
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

