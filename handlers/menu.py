from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from keyboards.all_kb import main_kb
from keyboards.inline_kbs import main_loader_kb, goback_actions_kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from utils.script import process_document_by_option
import asyncio
import os

from filters.admin_check import IsAdmin
from create_bot import admins, download_dir, bot, upload_notification_recievers

menu_router = Router()


class DocumentProcessing(StatesGroup):
    option = State()
    document = State()
    bot_error_msg_id = State()
    bot_back_msg_id = State()
    bot_early_doc_msg_id = State()


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
    await state.set_state(DocumentProcessing.option)


@menu_router.message(F.text == "🛟Поддержка")
async def show_support_options(message: Message):
    await message.delete()
    await message.answer(
        text="🐞Если у вас возникли трудности с работой бота:\n👉🏾Вы не можете загрузить документ\n👉🏾У вас проблема с навигацией по меню\n👉🏾Возникла ошибка при работе бота\n💬Для начала попробуйте перезапустить бота, командой /restart.\nЕсли это не помогло, напишите разработчику @Bobflipflop\n\n❓Если у вас возникли вопросы, по поводу загружаемых данных напишите свой вопрос - @mkuzhlev",
        reply_markup=main_kb(message.from_user.id),
    )

@menu_router.message(F.text == "⚙️Настройки")
async def show_support_options(message: Message):
    await message.delete()
    await message.answer(
        text="Данная функция пока не доступна. ☹",
        reply_markup=main_kb(message.from_user.id),
    )


@menu_router.message(Command("restart"))
async def restart_bot(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🔄Состояние сброшено!", reply_markup=main_kb(message.from_user.id)
    )


@menu_router.callback_query(F.data == "change_mind")
async def process_change_mind(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    bot_error_msg_id = data.get("bot_error_msg_id")

    await call.message.delete()
    if bot_error_msg_id:
        await call.bot.delete_message(
            chat_id=call.message.chat.id, message_id=bot_error_msg_id
        )
    back_msg = await call.message.answer(
        text="Возвращаю вас к меню.", reply_markup=main_kb(call.from_user.id)
    )
    await state.clear()
    await state.update_data(bot_back_msg_id=back_msg.message_id)


@menu_router.message(F.text, DocumentProcessing.option)
async def process_option_choice(message: Message):
    await message.delete()


@menu_router.message(F.document, DocumentProcessing.option)
async def process_option_choice(message: Message, state: FSMContext):
    data = await state.get_data()
    bot_early_doc_msg_id = data.get("bot_early_doc_msg_id")

    await message.delete()
    if bot_early_doc_msg_id:
        await bot.delete_message(message.chat.id, bot_early_doc_msg_id)
        await state.update_data(bot_early_doc_msg_id=None)

    new_msg = await message.answer(
        text="⬆️Сначала выберите тип дашборда для загрузки данных."
    )
    await state.update_data(bot_early_doc_msg_id=new_msg.message_id)


@menu_router.callback_query(F.data, DocumentProcessing.option)
async def process_option_choice(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    bot_early_doc_msg_id = data.get("bot_early_doc_msg_id")

    if bot_early_doc_msg_id:
        await bot.delete_message(call.message.chat.id, bot_early_doc_msg_id)
        await state.update_data(bot_early_doc_msg_id=None)

    option_name = call.data
    await state.update_data(option=option_name)
    await call.message.edit_text(
        text=f"Выбран дашборд <b>{option_name}</b>. Отправьте документ вложением, в следующем сообщении.",
        reply_markup=goback_actions_kb(),
    )
    await state.set_state(DocumentProcessing.document)


@menu_router.callback_query(F.data == "back", DocumentProcessing.document)
async def process_back_button(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    bot_error_msg_id = data.get("bot_error_msg_id")
    if bot_error_msg_id:
        await call.bot.delete_message(
            chat_id=call.message.chat.id, message_id=bot_error_msg_id
        )
    await call.message.edit_text(
        "Выберите дашборд, для которого вы хотите загрузить данные:",
        reply_markup=main_loader_kb(),
    )
    await state.update_data(bot_error_msg_id=None)
    await state.set_state(DocumentProcessing.option)


@menu_router.message(~F.document, DocumentProcessing.document)
async def process_document(message: Message, state: FSMContext):
    data = await state.get_data()
    bot_error_msg_id = data.get("bot_error_msg_id")
    await message.delete()
    if bot_error_msg_id:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_error_msg_id)
    error_message = await message.answer("Пожалуйста, отправьте документ.")
    await state.update_data(bot_error_msg_id=error_message.message_id)
    await state.set_state(DocumentProcessing.document)


@menu_router.message(F.document, DocumentProcessing.document)
async def process_document(message: Message, state: FSMContext):
    data = await state.get_data()
    dshb_name = data.get("option")

    if not message.document.file_name.endswith((".xlsx",)):
        await message.answer(
            "Пожалуйста, отправьте файл в формате Excel. Поддерживаемые расширения файлов .xlsx"
        )
        return

    # Getting file info
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_name = message.document.file_name

    # Downloading
    try: 
        downloaded_file = await bot.download_file(file_path)
        os.makedirs(download_dir, exist_ok=True)
        local_file_path = os.path.join(download_dir, f"{file_name}")
        with open(local_file_path, "wb") as new_file:
            new_file.write(downloaded_file.read())
    except Exception as e:
        print(f'СОХРАНЕНИЕ ФАЙЛА - ОШИБКА: {e}')

    # End download process
    data = await state.get_data()

    # result = process_document_by_option(
    #     local_file_path, local_file_path, data.get("option")
    # )
    caption_message = f"📄 Вам пришел новый документ!\n\n<b>Для дашборда:</b> {dshb_name}\n<b>Отправитель:</b> {message.from_user.full_name}, @{message.from_user.username or 'не указан'}"

    for user_id in upload_notification_recievers:
        try:
            await bot.send_document(
                chat_id=user_id,  # ID чата пользователя
                document=file_id,  # Открываем сохраненный файл
                caption=caption_message,  # Необязательный текст под файлом
            )
        except Exception as e:
            print(e)

        await asyncio.sleep(0.5)
    await message.answer("🟢Документ был отправлен ответственному лицу")
    await state.clear()
