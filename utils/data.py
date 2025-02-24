from aiogram.filters.callback_data import CallbackData

# Названия кнопок по дашбордам
dashboard_names = [
    "АИП",
    "ОЭП",
    "КОК",
    "ФНС",
    "КЦР",
    "ОИВ",
    "Соцзащита",
    "Гумманитарная помощь СВО",
    "Новый ФНС",
    "Импортозамещение",
]


# Менюшка
class MenuCallback(CallbackData, prefix="menu"):
    level: str
    option: str


menu_structure = {
    "main": {
        "Просмотр": "show",
    },
    "show": {
        "Админы": "admins",
        "Получатели": "recievers",
        "Белый список": "whitelist",
        "Назад": "main",
    },
}


# CF для принятия запросов
class RegistrationCallback(CallbackData, prefix="reg"):
    action: str
    user_id: int
