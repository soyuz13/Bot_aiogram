import json
import pprint
import logging
from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command, Text, CommandObject
from filters.admin_filters import IsAdmin
from typing import Literal
from models.users import Users, Admins
from markups.inline_keyboards import any_users_keyboard, AnyUsersList

logger = logging.getLogger('logs.admin_handlers')

router = Router()
router.message.filter(IsAdmin())


@router.message(Command("start"))
async def start_handler(msg: Message, *args, **kwargs):
    logger.info(f'{msg.from_user.id} - /start')

    await msg.answer("Привет! Это служебный бот SplitHall.\n"
                     "Команды:\n"
                     "/help - список команд\n"
                     "/nevatom - запуск запроса цен на сайте Nevatom\n\n"
                     )


@router.message(Command("help"))
async def start_handler(msg: Message, *args, **kwargs):
    logger.info(f'{msg.from_user.id} - /help')
    await msg.answer("Команды администратора:\n"                     
                     "/adduser id - добавление пользователя с id\n"
                     "/addadmin id - добавление администратора с id\n"
                     "/userlist - список пользователей\n"
                     "/adminlist - список админов\n"
                     "/clearusers - удаление всех пользователей\n"
                     "/clearadmins - удаление всех админов, кроме твоего\n"
                     )


@router.message(Command(commands=["adduser", 'addadmin']))
async def add_handler(msg: Message, command: CommandObject, bot: Bot, *args, **kwargs):
    logger.info(f'{msg.from_user.id} - /adduser or admin')
    if not command.args:
        await msg.reply('После команды через пробел введите добавляемый id')
        return
    if not command.args.isdecimal():
        await msg.reply('id пользователя должно быть числом. Проверьте еще раз')
        return

    user_id = int(command.args)
    try:
        await bot.send_message(user_id, '👋 Вы добавлены в группу бота SplitHall!')
    except Exception as ex:
        await bot.send_message(user_id, '❗ Ошибка добавления пользователя в бот SplitHall')
        print(ex)

        return

    if command.command == 'adduser':
        Users.add(user_id)
        text = 'Пользователь'
    else:
        Admins.add(user_id)
        text = 'Администратор'

    await msg.answer(f"{text} {user_id} добавлен")


@router.message(Command(commands=["userlist", 'adminlist']))
async def list_handler(msg: Message, command: CommandObject, bot: Bot, *args, **kwargs):
    logger.info(f'{msg.from_user.id} - /user-adminlist')
    if command.command == 'userlist':
        anyuser_list = Users.get_list()
        is_user_list = True
    else:
        anyuser_list = Admins.get_list()
        is_user_list = False

    if anyuser_list:
        await msg.answer(f'Список', reply_markup=any_users_keyboard(anyuser_list, is_user_list))
    else:
        await msg.answer(f'Список пользователей пуст')


@router.message(Command(commands=["clearusers", 'clearadmins']))
async def list_handler(msg: Message, command: CommandObject, bot: Bot, *args, **kwargs):
    logger.info(f'{msg.from_user.id} - /clearusers-admins')
    if command.command == 'clearusers':
        Users.clear()
        await msg.answer(f'Пользователи удалены')
    else:
        Admins.clear(msg.from_user.id)
        await msg.answer(f'Администраторы удалены')


@router.callback_query(AnyUsersList.filter())
async def anyuser_del_press(callback: CallbackQuery, callback_data: AnyUsersList):
    if callback_data.is_user_list:
        removed_id = Users.remove(callback_data.id)
        user_list = Users.get_list()
    else:
        if callback_data.id == callback.from_user.id:
            await callback.message.edit_text(text=f'Свой id не может быть удален')
            return
        removed_id = Admins.remove(callback_data.id)
        user_list = Admins.get_list()
    if user_list:
        await callback.message.edit_text(text=f'Удален {removed_id}', reply_markup=any_users_keyboard(user_list, callback_data.is_user_list))
    else:
        await callback.message.edit_text(text=f'Удален {removed_id}. Список пользователей пуст')


@router.callback_query(Text(text=['CANCEL']))
async def anyuser_cancel_press(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)


