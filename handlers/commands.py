from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from keyboards.all_kb import main_kb
from aiogram.fsm.context import FSMContext


commands_router = Router()


@commands_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
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
