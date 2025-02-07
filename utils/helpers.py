from aiogram import Bot
from aiogram.types import Message, Chat
from create_bot import download_dir
from create_bot import upload_notification_recievers
from create_bot import bot
from keyboards.all_kb import main_kb
import os
import asyncio


async def download_document(bot: Bot, file_path: str, file_name: str) -> str:
    try:
        downloaded_file = await bot.download_file(file_path)
        os.makedirs(download_dir, exist_ok=True)
        local_file_path = os.path.join(download_dir, f"{file_name}")
        with open(local_file_path, "wb") as new_file:
            new_file.write(downloaded_file.read())
        return local_file_path
    except Exception as e:
        print(f"СОХРАНЕНИЕ ФАЙЛА - ОШИБКА: {e}")

    # caption_message = f"📄 Вам пришел новый документ!\n\n<b>Для дашборда:</b> {dshb_name}\n<b>Отправитель:</b> {message.from_user.full_name}, @{message.from_user.username or 'не указан'}"


async def send_document(
    file_id: str,
    message: Message,
    caption_text: str,
    bot: Bot = bot,
    delete_message_timeout: int = 1,
    show_progress: bool = True,
):
    num_reciever_users = len(upload_notification_recievers)
    sending_text = f"🛫 Отправляю документ...\nПрогресс: {'⚪️' * num_reciever_users}"
    if not show_progress:
        sending_text = sending_text.split("\n")[0]

    sending_msg = await message.answer(text=sending_text)
    ids_without_send = []

    for user_id in upload_notification_recievers:
        try:
            await bot.send_document(
                chat_id=user_id,  # ID чата пользователя
                document=file_id,  # Открываем сохраненный файл
                caption=caption_text,  # Необязательный текст под файлом
            )
            if show_progress:
                sending_text = sending_text.replace("⚪️", "🟢", 1)
                await bot.edit_message_text(
                    text=sending_text,
                    chat_id=message.chat.id,
                    message_id=sending_msg.message_id,
                )
        except Exception as e:
            print(e)
            ids_without_send.append(user_id)
            if show_progress:
                sending_text = sending_text.replace("⚪️", "🔴", 1)
                await bot.edit_message_text(
                    text=sending_text,
                    chat_id=message.chat.id,
                    message_id=sending_msg.message_id,
                )

        await asyncio.sleep(0.2)

    await asyncio.sleep(delete_message_timeout)
    await bot.delete_message(chat_id=message.chat.id, message_id=sending_msg.message_id)

    return ids_without_send
