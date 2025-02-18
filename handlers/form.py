from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.chat_action import ChatActionSender

from keyboards.all_kb import main_kb
from aiogram.fsm.context import FSMContext
from db_handler.db_funk import get_user_info
from handlers.states import States

form_router = Router()


@form_router.message(F.text, States.form_full_name)
async def capture_fullname(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Отлично, из какой вы организации?")
    await state.set_state(States.form_org_name)


@form_router.message(F.text, States.form_org_name)
async def capture_orgname(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Проверьте свои данные: ", reply_markup=)
    await state.set_state(States.check_state)


@form_router.message(F.text, States.form_org_name)
async def capture_orgname(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Проверьте свои данные: ")
    await state.set_state(States.form_org_name)
