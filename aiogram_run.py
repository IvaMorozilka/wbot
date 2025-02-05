import asyncio
from create_bot import bot, dp, scheduler
from handlers.start import start_router
from handlers.document import document_router
from handlers.menu import menu_router
from utils.commands import set_commands
# from work_time.time_func import send_time_msg


async def main():
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()
    dp.include_routers(start_router, document_router, menu_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    await set_commands(bot)


if __name__ == "__main__":
    asyncio.run(main())
