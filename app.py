from asyncio import sleep

from utils.db_api.add_to_database import add_items, uploadPhoto
from utils.db_api.database import create_db
from utils.misc.set_bot_command import set_default_commands

async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await create_db()
    await sleep(10)
    await add_items()
    await sleep(10)
    await uploadPhoto()
    await set_default_commands(dp)
if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp
    executor.start_polling(dp, on_startup=on_startup)

