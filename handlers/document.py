from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from keyboards.all_kb import main_kb
from keyboards.inline_kbs import goback_actions_kb, main_loader_kb
from create_bot import bot, upload_notification_recievers
from utils.excel_helpers.checker import check_document_by_option
from utils.helpers import download_document, send_document


document_router = Router()


class DocumentProcessing(StatesGroup):
    waiting_for_option = State()
    waiting_for_document = State()


@document_router.callback_query(F.data == "change_mind")
async def process_change_mind(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    bot_error_msg_id = data.get("bot_error_msg_id")

    await call.message.delete()
    if bot_error_msg_id:
        await call.bot.delete_message(
            chat_id=call.message.chat.id, message_id=bot_error_msg_id
        )
    back_msg = await call.message.answer(
        text="Возвращаю вас в меню.", reply_markup=main_kb(call.from_user.id)
    )
    await state.clear()
    await state.update_data(bot_back_msg_id=back_msg.message_id)


@document_router.message(F.text, DocumentProcessing.waiting_for_option)
async def process_option_choice(message: Message):
    await message.delete()


@document_router.message(F.document, DocumentProcessing.waiting_for_option)
async def process_option_choice(message: Message, state: FSMContext):  # noqa: F811
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


@document_router.callback_query(F.data, DocumentProcessing.waiting_for_option)
async def process_option_choice(call: CallbackQuery, state: FSMContext):  # noqa: F811
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
    await state.set_state(DocumentProcessing.waiting_for_document)


@document_router.callback_query(
    F.data == "back", DocumentProcessing.waiting_for_document
)
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
    await state.set_state(DocumentProcessing.waiting_for_option)


@document_router.message(~F.document, DocumentProcessing.waiting_for_document)
async def process_document(message: Message, state: FSMContext):
    data = await state.get_data()
    bot_error_msg_id = data.get("bot_error_msg_id")
    await message.delete()
    if bot_error_msg_id:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_error_msg_id)
    error_message = await message.answer("Пожалуйста, отправьте документ.")
    await state.update_data(bot_error_msg_id=error_message.message_id)
    await state.set_state(DocumentProcessing.waiting_for_document)


@document_router.message(F.document, DocumentProcessing.waiting_for_document)
async def process_document(message: Message, state: FSMContext):  # noqa: F811
    data = await state.get_data()
    dshb_name = data.get("option")
    bot_invalid_filef_msg_id = data.get("bot_invalid_filef_msg_id")

    if bot_invalid_filef_msg_id:
        await bot.delete_message(
            chat_id=message.chat.id, message_id=bot_invalid_filef_msg_id
        )

    if not message.document.file_name.endswith((".xlsx", ".xlsm", ".xltx", ".xltm")):
        await message.delete()
        new_msg = await message.answer(
            "Пожалуйста, отправьте файл в формате таблиц Excel. \nℹ️Поддерживаемые расширения файлов xlsx/xlsm/xltx/xltm"
        )
        await state.update_data(bot_invalid_filef_msg_id=new_msg.message_id)
        return

    # Getting file info
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_name = message.document.file_name

    # Downloading
    local_file_path = await download_document(bot, file_path, file_name)

    # 1 - Checking for correct headers
    result, error_msg = check_document_by_option(local_file_path, category=dshb_name)
    if not result:
        await message.answer(
            f"❌ Возникла проблема при проверке документа.\n\n{error_msg}\nℹ️ Пожалуйста, отправьте новый документ следующим сообщением",
            reply_markup=goback_actions_kb(),
        )
        return

    # Sending ...
    caption_text = f"📄 Вам пришел новый документ!\n\n<b>Для дашборда:</b> {dshb_name}\n<b>Отправитель:</b> {message.from_user.full_name}, @{message.from_user.username or 'не указан'}"
    users_ids_without_send = await send_document(file_id, message, caption_text)
    user_names = ["Без базы данных упоминнание по id недоступно"]
    num_reciever_users = len(upload_notification_recievers)
    sending_text = f"Отправляю документ...\nСтатус: {'⚪️' * num_reciever_users}"
    sending_msg = await message.answer(text=sending_text)

    for idx, user_id in enumerate(upload_notification_recievers):
        try:
            await bot.send_document(
                chat_id=user_id,  # ID чата пользователя
                document=file_id,  # Открываем сохраненный файл
                caption=caption_message,  # Необязательный текст под файлом
            )
            sending_text = sending_text.replace("⚪️", "🟢", 1)
            await bot.edit_message_text(
                text=sending_text,
                chat_id=message.chat.id,
                message_id=sending_msg.message_id,
            )
        except Exception as e:
            print(e)
            # Обновляем строку статуса с ошибкой
            sending_text = sending_text.replace("⚪️", "🔴", 1)
            await bot.edit_message_text(
                text=sending_text,
                chat_id=message.chat.id,
                message_id=sending_msg.message_id,
            )

        await asyncio.sleep(0.2)

    await asyncio.sleep(1)
    await bot.delete_message(chat_id=message.chat.id, message_id=sending_msg.message_id)
    await message.reply(
        "🏁Ваш документ был успешно отправлен! Возвращаю вас в меню.",
        reply_markup=main_kb(message.from_user.id),
    )
    # End sending
    # Clear state
    await state.clear()


# @document_router.message(F.document)
# async def handle_document(message: Message):
#     if not message.document.file_name.endswith((".xlsx")):
#         await message.answer("Пожалуйста, отправьте файл в формате Excel (.xlsx).")
#         return

#     async with ChatActionSender.upload_document(chat_id=message.chat.id, bot=bot):
#         await message.answer("Файл получен. Обрабатываю...")

#         # Downloading...
#         file_id = message.document.file_id
#         file = await bot.get_file(file_id)
#         file_path = file.file_path
#         file_name = message.document.file_name

#         downloaded_file = await bot.download_file(file_path)
#         os.makedirs(download_dir, exist_ok=True)
#         local_file_path = os.path.join(download_dir, f"{file_name}")
#         with open(local_file_path, "wb") as new_file:
#             new_file.write(downloaded_file.read())
#         # End download process

#         # Start processing...
#         processed_file_path = os.path.join(download_dir, f"ОБРАБОТАН_{file_name}")
#         code, msg, warnings, logs = transform_pipeline(
#             local_file_path, processed_file_path
#         )
#         # Errors handle
#         if not code:
#             await message.answer(f"❌ Произошла ошибка при обработке файла ❌\n{msg}")
#         else:
#             if len(warnings) != 0:
#                 await message.answer(
#                     f"⚠️<b>Внимание</b>⚠️\n{''.join(f'{idx}. {item}\n' for idx, item in enumerate(warnings))}"
#                 )
#                 await message.answer("🪵Логи вычислений🪵\n")
#                 await message.answer(
#                     "Расчет (РУБЛИ)\n"
#                     + "\n".join(
#                         f"{key}: <code>={value}</code>"
#                         for key, value in logs[0].items()
#                     )
#                 )
#                 await message.answer(
#                     "Расчет (ПРОЦЕНТЫ)\n"
#                     + "\n".join(
#                         f"{key}: <code>={value}</code>"
#                         for key, value in logs[1].items()
#                     )
#                 )
#             await message.answer("✅<b>Файл успешно обработан ✅</b>")
#             await message.reply_document(document=FSInputFile(processed_file_path))

#         # Удаляем временные файлы
#         os.remove(local_file_path)
#         os.remove(processed_file_path)
