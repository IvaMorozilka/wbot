from aiogram import Router, F, Bot
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from handlers.states import States
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.all_kb import main_kb
from keyboards.inline_kbs import generate_settings_kb, settings_confirm_action_kb
from db_handler.db_funk import get_user_info, get_admins
from utils.constants import SettingsCallback
from handlers.states import SettingsStates
from utils.helpers import send_message_to_all_users

settings_router = Router()


@settings_router.callback_query(SettingsCallback.filter(F.option == "main"))
async def back_to_main_menu(call: CallbackQuery, callback_data: SettingsCallback):
    await call.message.edit_text(
        text="Главное меню", reply_markup=generate_settings_kb("main")
    )


@settings_router.callback_query(SettingsCallback.filter(F.level == "main"))
async def main_menu(call: CallbackQuery, callback_data: SettingsCallback):
    if callback_data.option == "show":
        await call.message.edit_text(
            text="Просмотр", reply_markup=generate_settings_kb(callback_data.option)
        )
    if callback_data.option == "send":
        await call.message.edit_text(
            text="Отправка сообщения",
            reply_markup=generate_settings_kb(callback_data.option),
        )


@settings_router.callback_query(SettingsCallback.filter(F.option == "back"))
async def go_back(call: CallbackQuery, callback_data: SettingsCallback):
    if callback_data.level == "show":
        await call.message.edit_text(
            text="Просмотр", reply_markup=generate_settings_kb("show")
        )
    elif callback_data.level == "send":
        await call.message.edit_text(
            text="Отправка сообщения", reply_markup=generate_settings_kb("send")
        )


@settings_router.callback_query(SettingsCallback.filter(F.level == "show"))
async def show_menu(call: CallbackQuery, callback_data: SettingsCallback, bot: Bot):
    if callback_data.option == "admins":
        await call.message.edit_text(
            text="Показал администраторов",
            reply_markup=generate_settings_kb("show", True),
        )
    elif callback_data.option == "recievers":
        await call.message.edit_text(
            text="Показал получателей", reply_markup=generate_settings_kb("show", True)
        )
    else:
        await call.message.edit_text(
            text="Показал кого то еще", reply_markup=generate_settings_kb("show", True)
        )


@settings_router.callback_query(SettingsCallback.filter(F.level == "send"))
async def send_menu(
    call: CallbackQuery, callback_data: SettingsCallback, bot: Bot, state: FSMContext
):
    if callback_data.option == "to_all":
        await call.message.edit_text(
            text="Напишите сообщение, которые вы хотите отправить всем пользователям бота",
            reply_markup=generate_settings_kb("send", True),
        )
        await state.set_state(SettingsStates.waiting_for_text)
    elif callback_data.option == "to_smb":
        await call.message.edit_text(
            text="Пока недоступно", reply_markup=generate_settings_kb("send", True)
        )
    elif callback_data.option == "confirm":
        data = await state.get_data()
        message_id = data.get("message_id_to_send")

        if message_id:
            # Отправляем сообщение всем пользователям
            successful, failed = await send_message_to_all_users(
                bot, message_id, call.from_user.id
            )

            await call.message.edit_text(
                text=f"👆 Ваше сообщение было отправлено всем пользователям\n{f'❌ Не удалось отправить {failed} пользователям' if failed > 0 else ''}",
                reply_markup=None,
            )

        await call.message.answer(
            text="Главное меню", reply_markup=generate_settings_kb("main")
        )
        await state.clear()

    elif callback_data.option == "cancel":
        await call.message.edit_text(
            text="Главное меню", reply_markup=generate_settings_kb("main")
        )
        await state.clear()


@settings_router.message(F.text, SettingsStates.waiting_for_text)
async def send_msg_to_all(message: Message, state: FSMContext):
    copy_message = await message.copy_to(chat_id=message.chat.id)
    await state.update_data(message_id_to_send=copy_message.message_id)
    await message.answer(
        text="Отправить данное сообшение всем?",
        reply_markup=settings_confirm_action_kb(level="send"),
    )
