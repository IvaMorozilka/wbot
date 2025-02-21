import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.client.session.aiohttp import AiohttpSession
from asyncpg_lite import DatabaseManager


session = None
if not config("DEV"):
    session = AiohttpSession(proxy=config("PROXY_URL"))

scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
ADMINS = [int(admin_id) for admin_id in config("ADMINS").split(",")]
secret_key = config("AUTH_KEY")
# DB
pg_manager = DatabaseManager(
    db_url=config("DATABASE_URL"),
    deletion_password=config("DEL_PASWD"),
    log_level="INFO",
    echo=False,
)

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
