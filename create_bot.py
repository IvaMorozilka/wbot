import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os
from aiogram.client.session.aiohttp import AiohttpSession

session = None
if not config("DEV"):
    session = AiohttpSession(proxy=config("PROXY_URL"))

scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
admins = [int(admin_id) for admin_id in config("ADMINS").split(",")]
upload_notification_recievers = [
    int(user_id) for user_id in config("UPLOAD_NOTIFICATION_RECEIVERS").split(",")
]

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

download_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")

bot = Bot(
    token=config("TOKEN"),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    session=session,
)
dp = Dispatcher(storage=MemoryStorage())
