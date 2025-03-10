from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.constants import (
    DASHBOARD_NAMES,
    MENU_STRUCTURE,
    MenuCallback,
    RegistrationCallback,
)


def main_loader_kb():
    builder = InlineKeyboardBuilder()
    for text, callback in DASHBOARD_NAMES:
        builder.button(text=text, callback_data=callback)
    builder.adjust(3, 3, 1, 1, 1, 1)
    return builder.as_markup()


def goback_actions_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Отменить выбор", callback_data="back")],
            # [InlineKeyboardButton(text="Обратно в меню", callback_data="goto_menu")],
        ]
    )


def generate_settings_kb(level, back=False):
    builder = InlineKeyboardBuilder()
    if not back:
        for option, callback in MENU_STRUCTURE[level].items():
            builder.button(
                text=option, callback_data=MenuCallback(level=level, option=callback)
            )
        builder.adjust(1, True)
        return builder.as_markup()
    else:
        builder.button(
            text="Назад", callback_data=MenuCallback(level=level, option="back")
        )
        builder.adjust(1, True)
        return builder.as_markup()


def register_request_kb(user_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="✅ Принять",
        callback_data=RegistrationCallback(
            action="a",
            user_id=user_id,
        ),
    )
    builder.button(
        text="❌ Отклонить",
        callback_data=RegistrationCallback(
            action="r",
            user_id=user_id,
        ),
    )
    builder.adjust(1, 1)
    return builder.as_markup()
