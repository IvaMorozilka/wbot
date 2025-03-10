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


# Менюшка
class MenuCallback(CallbackData, prefix="menu"):
    level: str
    option: str


MENU_STRUCTURE = {
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


# CF для интрукций
class InstructionsCallback(CallbackData, prefix="instr"):
    option: str
    image: str


INSTRUCTIONS_IMAGES = {"ГуманитарнаяПомощьСВО": "assets/ha.jpg"}
