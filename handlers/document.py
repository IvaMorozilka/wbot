from aiogram import Router, F
from aiogram.types import Document, Message
from aiogram.utils.chat_action import ChatActionSender
from aiogram.types import FSInputFile
import os

from utils.script import transform_pipeline
from create_bot import bot, download_dir


document_router = Router()


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
