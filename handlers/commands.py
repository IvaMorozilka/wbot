from aiogram import Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

from keyboards.all_kb import main_kb
from aiogram.fsm.context import FSMContext
from db_handler.db_funk import get_user_info
from handlers.states import States
from filters.user_auth_check import IsAuthorized
from db_handler.db_funk import get_user_info
from create_bot import secret_key

commands_router = Router()


@commands_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    user_info = await get_user_info(message.from_user.id)
    if user_info:
        await message.answer(
            text="Воспользуйтесь меню 📋",
            reply_markup=main_kb(message.from_user.id),
        )
    else:
        await message.answer("Введите код авторизации 🔐")
        await state.set_state(States.form_auth_key)


@commands_router.message(Command("restart"))
async def restart_bot(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🔄Состояние сброшено!", reply_markup=main_kb(message.from_user.id)
    )
