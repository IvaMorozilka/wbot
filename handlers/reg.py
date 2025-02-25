from aiogram import Router, F
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from datetime import datetime

from keyboards.all_kb import main_kb
from keyboards.inline_kbs import register_request_kb
from aiogram.fsm.context import FSMContext
from db_handler.db_funk import (
    insert_user,
    get_admins,
    send_registration_request,
    get_update_request_info,
)
from handlers.states import States
from create_bot import ADMINS, bot
from utils.data import RegistrationCallback


reg_router = Router()


@reg_router.message(F.text, States.form_full_name)
async def capture_fullname(message: Message, state: FSMContext):
    await state.update_data(
        {
            "full_name": message.text,
            "user_id": message.from_user.id,
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
                [
                    InlineKeyboardButton(
                        text="✅ Отправить запрос", callback_data="correct"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="❌ Заполнить сначала",
                        callback_data="incorrect",
                    )
                ],
            ]
        ),
    )
    await state.set_state(States.check_state)


@reg_router.callback_query(F.data == "correct", States.check_state)
async def finish_form(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    if call.from_user.id in ADMINS:
        await insert_user({**data, "admin": True})
        await call.message.edit_text(
            "Регистрация успешна. Вы были указаны в списке Администраторов 👨🏻‍💻"
        )
    else:
        await send_registration_request({**data, "admin": False, "status": 0})
        await call.message.edit_text(
            text="Ваш запрос был направлен Администраторам 📨 Ожидайте уведомления с решением.",
            reply_markup=None,
        )
        admins_info = await get_admins()
        for user_id in [admin["user_id"] for admin in admins_info]:
            await bot.send_message(
                chat_id=user_id,
                text=f"<b>Новый запрос на регистрацию</b> 🙋‍♂️\n\nДата и время: {datetime.now().strftime('%d-%m-%y %H:%M')}\nИмя: {data.get('full_name')}{data.get('username')}\nОрганизация: {data.get('org_name')}",
                reply_markup=register_request_kb(data.get("user_id")),
            )
    await state.clear()


@reg_router.callback_query(F.data == "incorrect", States.check_state)
async def finish_form(call: CallbackQuery, state: FSMContext):  # noqa: F811
    await call.answer()
    await call.message.answer("Хорошо, давайте начнем заново.")
    await call.message.answer(
        "Отправьте свое полное ФИО, например: Иванов Иван Иванович"
    )
    await state.set_state(States.form_full_name)


@reg_router.callback_query(RegistrationCallback.filter(F.action == "a"))
async def accept_registration(call: CallbackQuery, callback_data: RegistrationCallback):
    user_info = await get_update_request_info(user_id=callback_data.user_id, status=1)

    if user_info.get("processed"):
        await call.message.edit_text("Заявка уже обработана другим Администратором ℹ️")
        return
    # Делаем вставку без status и processed
    await insert_user(
        {k: v for k, v in user_info.items() if k not in {"status", "processed"}}
    )
    await process_request(user_info.get("user_id"))
    await call.message.edit_text(
        f"Пользователь {user_info.get('full_name')}, {user_info.get('username')} принят ✅"
    )

    await bot.send_message(
        chat_id=callback_data.user_id,
        text="Ваш запрос был принят 🥳. Теперь вы можете загружать данные.",
        reply_markup=main_kb(),
    )


@reg_router.callback_query(RegistrationCallback.filter(F.action == "r"))
async def reject_registration(call: CallbackQuery, callback_data: RegistrationCallback):
    user_info = await get_update_request_info(user_id=callback_data.user_id, status=2)

    if user_info.get("processed"):
        await call.message.edit_text("Заявка уже обработана другим Администратором ℹ️")
        return

    await call.message.edit_text(
        f"Пользователь {user_info.get('full_name')}, {user_info.get('username')} отклонен ⛔"
    )
    await process_request(user_info.get("user_id"))
    await bot.send_message(
        chat_id=callback_data.user_id,
        text="Ваш запрос был отклонен 😔",
        reply_markup=main_kb(),
    )
