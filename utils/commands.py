from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot):
    commands = [
        BotCommand(command="start", description="Запуск"),
        BotCommand(command="restart", description="Перезагрузка"),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
