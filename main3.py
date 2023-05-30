import asyncio
import logging
import ssl

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from aiohttp.web import run_app
from aiohttp.web_app import Application
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp.web_response import json_response
from aiohttp.web_request import Request

from config import TOKEN, APP_HOST, APP_PORT
from handlers import router
from aiogram.types import FSInputFile

application = Application()

DEVELOP = False

async def on_startup(bot: Bot, base_url: str):
    fil = FSInputFile('cert.pem')
    await bot.set_webhook(f"{base_url}/webhook", certificate=fil)


async def on_startup_develop(bot: Bot, base_url: str):
    print('Ставим Хук на девелоп')
    await bot.set_webhook(f"{base_url}/webhook")


async def demo_handler(request: Request):
    return json_response({"Проверка доступа к хосту": True})


def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp["base_url"] = 'https://' + APP_HOST + ':' + APP_PORT
    dp.startup.register(on_startup)

    dp.include_router(router)

    application["bot"] = bot
    application.router.add_get("/demo", demo_handler)

    bot.delete_webhook(drop_pending_updates=True)

    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot, list_callbackcodes=[], list_captions=[], list_urls=[]
        ).register(application, path="/webhook")

    setup_application(application, dp, bot=bot)

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain('cert.pem', 'private.key')

    run_app(application, host=APP_HOST, port=APP_PORT, ssl_context=ssl_context)


def main_develop():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp["base_url"] = 'https://d379-37-29-88-192.ngrok-free.app'
    dp.startup.register(on_startup_develop)

    dp.include_router(router)

    application["bot"] = bot
    application.router.add_get("/demo", demo_handler)

    bot.delete_webhook(drop_pending_updates=True)

    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot, list_callbackcodes=[], list_captions=[], list_urls=[]
        ).register(application, path="/webhook")

    setup_application(application, dp, bot=bot)

    run_app(application, host='127.0.0.1', port=8081)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    if DEVELOP:
        main_develop()
    else:
        main()
