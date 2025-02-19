from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from aiogram.utils.chat_action import ChatActionSender

from keyboards.all_kb import main_kb
from aiogram.fsm.context import FSMContext
from db_handler.db_funk import get_user_info, insert_user
from handlers.states import States


form_router = Router()


@form_router.message(F.text, States.form_full_name)
async def capture_fullname(message: Message, state: FSMContext):
    await state.update_data(
        {
            "full_name": message.text,
            "user_id": message.from_user.id,
            "chat_id": message.chat.id,
            "username": "@" + message.from_user.username,
        }
    )
    await message.answer("Отлично, из какой вы организации?")
    await state.set_state(States.form_org_name)


@form_router.message(F.text, States.form_org_name)
async def capture_orgname(message: Message, state: FSMContext):
    await state.update_data(org_name=message.text)
    data = await state.get_data()
    await message.answer(
        f"Проверьте свои данные:\n\n<b>ФИО</b>: {data.get('full_name')}\n<b>Огранизация</b>: {data.get('org_name')}",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="✅Все верно", callback_data="correct")],
                [
                    InlineKeyboardButton(
                        text="❌Заполнить сначала", callback_data="incorrect"
                    )
                ],
            ]
        ),
    )
    await state.set_state(States.check_state)


@form_router.callback_query(F.data == "correct", States.check_state)
async def finish_form(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await insert_user({**data, "admin": False})
    await call.message.edit_text(
        text="Благодарю за регистрацию! Данные успешно сохранены.", reply_markup=None
    )
    await state.clear()


@form_router.callback_query(F.data == "incorrect", States.check_state)
async def finish_form(call: CallbackQuery, state: FSMContext):  # noqa: F811
    await call.message.answer("Для начала представьтесь пожалуйста. Введите свое ФИО.")
    await state.set_state(States.form_full_name)
