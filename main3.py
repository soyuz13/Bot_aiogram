import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from aiohttp.web import run_app
from aiohttp.web_app import Application
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.types import MenuButtonWebApp, WebAppInfo
from aiohttp.web_response import json_response
from aiohttp.web_request import Request

from config import TOKEN, CHAT_ID, APP_BASE_URL
from handlers import router
from aiogram.types import FSInputFile

application = Application()


async def on_startup(bot: Bot, base_url: str):
    fil = FSInputFile('cert.pem')
    await bot.set_webhook(f"{base_url}/webhook", certificate=fil)
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(text="Open Menu", web_app=WebAppInfo(url=f"{base_url}/demo"))
    )


async def demo_handler(request: Request):
    print('Дошло')
    return json_response({"ok": True})


def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp["base_url"] = APP_BASE_URL
    dp.startup.register(on_startup)

    dp.include_router(router)

    application["bot"] = bot
    application.router.add_get("/demo", demo_handler)

    bot.delete_webhook(drop_pending_updates=True)

    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        ).register(application, path="/webhook")
    setup_application(application, dp, bot=bot)

    run_app(application, host="127.0.0.1", port=443)

    # await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(), mylist=[1,2,3])


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    main()
