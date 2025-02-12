from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.data import dashboard_names


def main_loader_kb():
    builder = InlineKeyboardBuilder()
    for name in dashboard_names:
        builder.button(text=name, callback_data=name)
    builder.adjust(3, 3, 1, 1, 1, 1)
    return builder.as_markup()


def goback_actions_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Отменить выбор", callback_data="back")],
            # [InlineKeyboardButton(text="Обратно в меню", callback_data="goto_menu")],
        ]
    )
