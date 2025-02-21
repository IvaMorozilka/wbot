from aiogram import Router, F
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)

from keyboards.all_kb import main_kb
from aiogram.fsm.context import FSMContext
from db_handler.db_funk import get_user_info, insert_user
from handlers.states import States
from filters.user_auth_check import IsAuthorized, users_cache
from create_bot import secret_key, ADMINS


reg_router = Router()


@reg_router.message(F.text, States.form_auth_key)
async def capture_authkey(message: Message, state: FSMContext):
    if message.text == secret_key:
        await message.answer("Ваше полное ФИО, например: Иванов Иван Иванович")
        await state.set_state(States.form_full_name)
    else:
        await message.answer("Ваш код авторазиции неверный, в доступе отказано.")
        await state.clear()


@reg_router.message(F.text, States.form_full_name)
async def capture_fullname(message: Message, state: FSMContext):
    await state.update_data(
        {
            "full_name": message.text,
            "user_id": message.from_user.id,
            "chat_id": message.chat.id,
            "username": f"{message.from_user.username if message.from_user.username else 'Не указан'}",
        }
    )
    await message.answer(f"{message.text}, из какой вы организации?")
    await state.set_state(States.form_org_name)


@reg_router.message(F.text, States.form_org_name)
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


@reg_router.callback_query(F.data == "correct", States.check_state)
async def finish_form(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if call.from_user.id in ADMINS:
        await insert_user({**data, "admin": True, "reciever": True})
    else:
        await insert_user({**data, "admin": False, "reciever": False})
    await call.message.edit_text(
        text="Благодарю, ваши Данные успешно сохранены.", reply_markup=None
    )
    await call.message.answer(
        "Воспользуйтесь меню 📋", reply_markup=main_kb(call.message.from_user.id)
    )
    await state.clear()


@reg_router.callback_query(F.data == "incorrect", States.check_state)
async def finish_form(call: CallbackQuery, state: FSMContext):  # noqa: F811
    await call.answer()
    await call.message.answer("Хорошо, давайте начнем заново.")
    await call.message.answer("Ваше полное ФИО, например: Иванов Иван Иванович")
    await state.set_state(States.form_full_name)
