from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from create_bot import admins


def main_kb(user_id):
    kb_list = [
        [KeyboardButton(text="⬇️Загрузить данные для дашборда")],
        [KeyboardButton(text="🛟Поддержка")],
    ]

    if user_id in admins:
        kb_list.append([KeyboardButton(text="⚙️Настройки")])

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Выберите категорию:",
    )
    return keyboard
