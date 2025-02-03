from aiogram import Router, F
from aiogram.types import Document, Message
from aiogram.utils.chat_action import ChatActionSender
from aiogram.types import FSInputFile
import os

from utils.script import transform_pipeline
from create_bot import bot



document_router = Router()


@document_router.message(F.document)
async def handle_document(message: Message):
    if not message.document.file_name.endswith((".xlsx")):
        await message.answer(
            "Пожалуйста, отправьте файл в формате Excel (.xlsx)."
        )
        return

    async with ChatActionSender.upload_document(chat_id=message.chat.id, bot=bot):
        await message.answer("Файл получен. Обрабатываю...")

        # Downloading...
        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        downloaded_file = await bot.download_file(file_path)

        download_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
        os.makedirs(download_dir, exist_ok=True)

        local_file_path = os.path.join(download_dir, f"{message.document.file_name}")
        with open(local_file_path, 'wb') as new_file:
            new_file.write(downloaded_file.read())
        # End download process
         

        
