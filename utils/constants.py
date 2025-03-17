from ast import main
from aiogram.filters.callback_data import CallbackData

# Названия кнопок по дашбордам
# (название кнопки, название колбэка)
DASHBOARD_NAMES = [
    ("АИП", "АИП"),
    ("ОЭП", "ОЭП"),
    ("КОК", "КОК"),
    ("ФНС", "ФНС"),
    ("КЦР", "КЦР"),
    ("ОИВ", "ОИВ"),
    ("Соцзащита", "Соцзащита"),
    ("Гуманитарная помощь СВО", "ГуманитарнаяПомощьСВО"),
    ("Новый ФНС", "НовыйФНС"),
    ("Импортозамещение", "Импортозамещение"),
]
DASHBOARD_CALLBACKS = [callback for _, callback in DASHBOARD_NAMES]

INSTRUCTIONS_IMAGES = {"ГуманитарнаяПомощьСВО": "assets/ha.png"}

SETTINGS_STRUCTURE = {
    "main": {
        "Просмотр": "show",
        "Отправить сообщение": "send",
    },
    "show": {
        "Админы": "admins",
        "Получатели": "recievers",
        "Белый список": "whitelist",
        "Назад": "main",
    },
    "send": {
        "Отправить всем": "to_all",
        "Отправить кому-то": "to_smb",
        "Назад": "main",
    },
}


# Менюшка
class SettingsCallback(CallbackData, prefix="menu"):
    level: str
    option: str


# CF для принятия запросов
class RegistrationCallback(CallbackData, prefix="reg"):
    action: str
    user_id: int
