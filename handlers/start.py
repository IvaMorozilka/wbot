from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from keyboards.all_kb import main_kb
from keyboards.inline_kbs import main_loader_kb
from aiogram.fsm.context import FSMContext

from filters.admin_check import IsAdmin
from create_bot import admins

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Бот для загрузки данных в дашборды. Воспользуйтесь меню.",
        reply_markup=main_kb(message.from_user.id),
    )
