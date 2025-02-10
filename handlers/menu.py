from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from handlers.states import States

from keyboards.inline_kbs import main_loader_kb
from keyboards.all_kb import main_kb

menu_router = Router()


@menu_router.message(F.text == "⬇️Загрузить данные для дашборда")
async def show_upload_options(message: Message, state: FSMContext):
    data = await state.get_data()
    bot_back_msg_id = data.get("bot_back_msg_id")
    await message.delete()
    if bot_back_msg_id:
        await bot.delete_message(message.chat.id, bot_back_msg_id)
    await state.clear()
    await message.answer(
        "Выберите дашборд, для которого вы хотите загрузить данные:",
        reply_markup=main_loader_kb(),
    )
    await state.set_state(DocumentProcessing.waiting_for_option)


@menu_router.message(F.text == "🛟Поддержка")
async def show_support_options(message: Message):
    await message.delete()
    await message.answer(
        text="🐞Если у вас возникли трудности с работой бота:\n👉🏾Вы не можете загрузить документ\n👉🏾У вас проблема с навигацией по меню\n👉🏾Возникла ошибка при работе бота\n💬Для начала попробуйте перезапустить бота, командой /restart.\nЕсли это не помогло, напишите разработчику @Bobflipflop\n\n❓Если у вас возникли вопросы, по поводу загружаемых данных напишите свой вопрос - @mkuzhlev",
        reply_markup=main_kb(message.from_user.id),
    )


@menu_router.message(F.text == "⚙️Настройки")
async def show_support_options(message: Message):  # noqa: F811
    await message.delete()
    await message.answer(
        text="Данная функция пока не доступна. ☹",
        reply_markup=main_kb(message.from_user.id),
    )
