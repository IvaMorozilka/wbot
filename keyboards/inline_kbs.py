from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.data import dashboard_names


def main_loader_kb():
    builder = InlineKeyboardBuilder()
    for name in dashboard_names:
        builder.button(text=name, callback_data=name)
    builder.button(text="Я передумал", callback_data="change_mind")
    builder.adjust(3, 3, 2, 2, 1)
    return builder.as_markup()


def back_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="back")]]
    )


def changed_mind_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Я передумал", callback_data="back")]
        ]
    )
