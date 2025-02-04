from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.data import dashboard_names


def main_loader_kb():
    builder = InlineKeyboardBuilder()
    for name in dashboard_names:
        builder.button(text=name, callback_data=name)
    builder.adjust(3, 3, 2, 2)
    return builder.as_markup()
