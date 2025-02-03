from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_loader_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="Данные ОЭП", url = "www.google.com")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
