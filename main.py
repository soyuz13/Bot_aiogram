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
from aiogram.types import MenuButtonWebApp, WebAppInfo, MenuButtonDefault

from config import TOKEN, APP_HOST, APP_PORT, DEVELOP, get_logger, TOKEN2
from handlers import user_handlers, admin_handlers
from aiogram.types import FSInputFile

application = Application()

logger = get_logger('logs')


async def on_startup(bot: Bot, base_url: str):
    await bot.delete_webhook(drop_pending_updates=True)
    fil = FSInputFile('cert.pem')
    await bot.set_webhook(f"{base_url}/webhook", certificate=fil)


async def on_exit(bot: Bot):
    await bot.delete_webhook()


async def on_startup_develop(bot: Bot, base_url: str, **kwargs):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(f"{base_url}/webhook")


async def demo_handler(request: Request):
    logger.info('Пришел get-запрос')
    return json_response({"Проверка доступа к хосту": True})


def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp["base_url"] = 'https://' + APP_HOST + ':' + APP_PORT

    logger.debug('Установка webhook...')
    dp.startup.register(on_startup)
    logger.debug('Webhook установлен')

    dp.include_router(admin_handlers.router)
    dp.include_router(user_handlers.router)

    application["bot"] = bot
    application.router.add_get("/demo", demo_handler)

    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot, list_callbackcodes=[], list_captions=[], list_urls=[]
        ).register(application, path="/webhook")

    setup_application(application, dp, bot=bot)

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain('cert.pem', 'private.key')

    logger.debug('Запуск приложения...')
    run_app(application, host=APP_HOST, port=APP_PORT, ssl_context=ssl_context)


def main_develop():
    bot = Bot(token=TOKEN2, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp["base_url"] = 'https://a711-188-162-228-231.ngrok-free.app'

    logger.info('Ставим Хук на девелоп')
    dp.startup.register(on_startup_develop)
    logger.info('Хук установлен')

    dp.include_router(admin_handlers.router)
    dp.include_router(user_handlers.router)

    application["bot"] = bot
    application.router.add_get("/demo", demo_handler)

    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot, list_callbackcodes=[], list_captions=[], list_urls=[], kb_msg_id=[]
        ).register(application, path="/webhook")

    setup_application(application, dp, bot=bot)

    try:
        run_app(application, host='127.0.0.1', port=8081)
        logger.info('Приложение завершено')
    except Exception as ex:
        logger.error(ex)


if __name__ == "__main__":
    if DEVELOP:
        main_develop()
    else:
        main()
