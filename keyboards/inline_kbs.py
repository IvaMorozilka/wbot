from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.data import dashboard_names


def main_loader_kb():
    builder = InlineKeyboardBuilder()
    for name in dashboard_names:
        builder.button(text=name, callback_data=name)
    # builder.button(text="Обратно в меню", callback_data="goto_menu")
    builder.adjust(1)
    return builder.as_markup()


def goback_actions_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Обратно, к выбору дашборда", callback_data="back"
                )
            ],
            # [InlineKeyboardButton(text="Обратно в меню", callback_data="goto_menu")],
        ]
    )
