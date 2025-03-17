from aiogram import Bot
from aiogram.types import Message, BufferedInputFile
import os
import asyncio
import io
import pandas as pd
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from create_bot import download_dir, bot
from db_handler.db_funk import get_admins, get_all_users


async def send_document(
    file_id: str,
    message: Message,
    caption_text: str,
    bot: Bot = bot,
    delete_message_timeout: int = 1,
    show_progress: bool = True,
):
    recievers = await get_admins()
    num_reciever_users = len(recievers)
    sending_text = f"🛫 Отправляю документ...\nПрогресс: {'⚪️' * num_reciever_users}"
    if not show_progress:
        sending_text = sending_text.split("\n")[0]

    sending_msg = await message.answer(text=sending_text)
    ids_without_send = []

    for user_id in [reciever["user_id"] for reciever in recievers]:
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

    return num_reciever_users, ids_without_send


async def send_message_to_all_users(
    bot: Bot, message_id: int, from_chat_id: int
) -> tuple[int, int]:
    # Получаем всех пользователей из базы данных
    users = await get_all_users()
    users = [user.get("user_id") for user in users]
    # Фильтр, чтобы не дублировалось сообщение в чат
    users = list(filter(lambda user: user != from_chat_id, users))

    successful = 0
    failed = 0

    for user_id in users:
        try:
            # Копируем сообщение пользователю
            await bot.copy_message(
                chat_id=user_id,
                from_chat_id=from_chat_id,
                message_id=message_id,
                disable_notification=False,
            )
            successful += 1
            # Небольшая задержка для избежания блокировки API
            await asyncio.sleep(0.05)
        except TelegramBadRequest:
            # Обработка ошибки если пользователь заблокировал бота
            failed += 1
        except Exception as e:
            # Логирование других ошибок
            print(f"Error sending message to {user_id}: {e}")
            failed += 1

    return successful, failed
