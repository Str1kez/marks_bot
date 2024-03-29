async def on_startup(dispatcher):
    import app.filters
    import app.handlers
    import app.middlewares
    from app.utils import on_startup_notify, set_default_commands

    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == "__main__":
    from aiogram import executor

    from app.loader import dp

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
