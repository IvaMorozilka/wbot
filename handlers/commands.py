from aiogram import Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

from keyboards.all_kb import main_kb
from aiogram.fsm.context import FSMContext
from db_handler.db_funk import get_user_info
from handlers.states import States

commands_router = Router()


@commands_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        user_info = await get_user_info(message.from_user.id)

    if not user_info:
        await message.answer("Для начала представьтесь пожалуйста. Введите свое ФИО.")
        await state.set_state(States.form_full_name)
    else:
        await message.answer(
            text="Воспользуйтесь меню.",
            reply_markup=main_kb(message.from_user.id),
        )


@commands_router.message(Command("restart"))
async def restart_bot(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🔄Состояние сброшено!", reply_markup=main_kb(message.from_user.id)
    )
