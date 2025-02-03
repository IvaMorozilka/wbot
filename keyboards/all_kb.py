from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from create_bot import admins


def main_kb(user_telegram_id):
    kb_list = [[KeyboardButton(text="Данные для ОЭП")]]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Какие данные вы загружаете?",
    )
    return keyboard
