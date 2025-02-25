from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from handlers.states import States

from keyboards.inline_kbs import main_loader_kb, generate_settings_kb
from keyboards.all_kb import main_kb
from utils.data import MenuCallback
from db_handler.db_funk import get_user_info, get_admins


menu_router = Router()


@menu_router.message(F.text == "⬇️Загрузить данные")
async def show_upload_options(message: Message, state: FSMContext):
    await state.clear()
    user_info = await get_user_info(message.from_user.id)
    if user_info:
        await message.answer(
            "Выберите дашборд, для которого вы хотите загрузить данные:",
            reply_markup=main_loader_kb(),
        )
        await state.set_state(States.waiting_for_option)
    else:
        await message.answer(
            "Для начала загрузки вам нужно представиться. Воспользуйтесь командой /start"
        )


@menu_router.message(F.text == "🛟Поддержка")
async def show_support_options(message: Message):
    await message.answer(
        text="🐞Если у вас возникли трудности с работой бота:\n👉🏾Вы не можете загрузить документ\n👉🏾У вас проблема с навигацией по меню\n👉🏾Возникла ошибка при работе бота\n💬Для начала попробуйте перезапустить бота, командой /restart.\nЕсли это не помогло, напишите разработчику @Bobflipflop\n\n❓Если у вас возникли вопросы, по поводу загружаемых данных напишите свой вопрос - @mkuzhlev",
        reply_markup=main_kb(),
    )


@menu_router.message(F.text == "⚙️Настройки")
async def show_settings(message: Message):
    admins = await get_admins()
    if any(message.from_user.id in admin.values() for admin in admins):
        await message.answer(
            text="Настройки:",
            reply_markup=generate_settings_kb("main"),
        )
    else:
        await message.answer("Только для администраторов 👨🏻‍💼")


@menu_router.callback_query(MenuCallback.filter(F.option == "main"))
async def back_to_main_menu(call: CallbackQuery, callback_data: MenuCallback):
    await call.message.edit_text(
        text="Главное меню", reply_markup=generate_settings_kb("main")
    )


@menu_router.callback_query(MenuCallback.filter(F.level == "main"))
async def main_menu(call: CallbackQuery, callback_data: MenuCallback):
    if callback_data.option == "show":
        await call.message.edit_text(
            text="Просмотр", reply_markup=generate_settings_kb(callback_data.option)
        )


@menu_router.callback_query(
    MenuCallback.filter(F.level == "show" and F.option == "back")
)
async def go_back(call: CallbackQuery):
    await call.message.edit_text(
        text="Просмотр", reply_markup=generate_settings_kb("show")
    )


@menu_router.callback_query(MenuCallback.filter(F.level == "show"))
async def show_menu(call: CallbackQuery, callback_data: MenuCallback, bot: Bot):
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
