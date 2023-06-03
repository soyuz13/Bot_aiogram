import pprint
import pickle
import logging
from datetime import datetime
from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command, Text
from zoneinfo import ZoneInfo
from markups.inline_keyboards import groups_keyboard, subgroups_keyboard, MenuCD, edit_keyboard
from parsing import parsing_nevatom

logger = logging.getLogger('logs.user_handlers')

router = Router()
CATALOG = []


def get_group_name(category: int):
    return list(filter(lambda y: y.id == category, CATALOG))[0].caption


def get_attr(category: int, subcategory: int, param: str):
    a = list(filter(lambda x: x.id == category, CATALOG))[0].subgroups
    b = list(filter(lambda y: y.id == subcategory, a))[0]
    dic_ = {'caption': b.__getattribute__('caption'),
            'caption_translit': b.__getattribute__('caption_translit'),
            'url_path': b.__getattribute__('url_path'),
            # 'subgroups': b.__getattribute__('subgroups')
            }
    return dic_[param]


@router.message(Command("start"))
async def start_handler1(msg: Message, bot: Bot, *args, **kwargs):
    logger.info(f'{msg.from_user.id} - /start')
    await msg.answer("Привет! Это служебный бот.\n"
                     "Команды:\n"
                     "/help - список команд (в разработке)\n"
                     "/nevatom - запуск запроса цен на сайте Nevatom")


@router.message(Command("help"))
async def start_handler1(msg: Message, *args, **kwargs):
    logger.info(f'{msg.from_user.id} - /help')
    await msg.answer("Для сбора информации о ценах с сайта Nevatom нужно выбрать интересующие подкатегории. "
                     "Для этого нажать на нужный раздел каталога ниже, после чего нажать на нужную подкатегорию.  "
                     "Она добавится в список на запрос цен.\n"
                     "Вернуться к разделам можно по кнопке '⬅️ НАЗАД В КАТАЛОГ'.\n"
                     "Выбери таким образом все нужные подкатегории и запусти запрос из каталога по кнопке '🚀 ЗАПУСТИТЬ ПОИСК'.\n"
                     "Удалить из списка лишнее можно по кнопке '💬 РЕДАКТИРОВАТЬ ВЫБРАННОЕ'")


@router.message(Command("nevatom"))
async def start_handler2(msg: Message, list_callbackcodes: list, list_captions: list, list_urls: list):
    logger.info(f'{msg.from_user.id} - /nevatom')
    temp_answer = await msg.answer("Запрос каталога сайта...")

    if parsing_nevatom.get_catalog():
        with open('files/nevatom_catalog.pickle', 'rb') as fil:
            global CATALOG
            CATALOG = pickle.load(fil)
    else:
        error_msg = 'Ошибка запроса каталога на сайте Nevatom, попробуйте позже'
        logger.error(f'{msg.from_user.id} - {error_msg}')
        await msg.answer(error_msg)
        return

    list_callbackcodes.clear()
    list_captions.clear()
    list_urls.clear()
    await msg.answer("Выбери раздел каталога, затем нажми нужную подкатегорию, "
                     "она добавится в список на запрос цен.\n"
                     "Удалить лишнее из списка - нажми '💬 РЕДАКТИРОВАТЬ СПИСОК...'\n"
                     "Вернуться к разделам - нажми '⬅️ НАЗАД'\n"
                     "Выбери так все нужные подкатегории и нажми '🚀 ЗАПУСК'")
    await temp_answer.delete()
    await msg.answer("КАТАЛОГ",
                     reply_markup=groups_keyboard(CATALOG))


# Обрабатываем нажатие кнопок каталога
@router.callback_query(MenuCD.filter(F.level == '0'))
async def process_catalog_button_press(callback: CallbackQuery, callback_data: MenuCD, list_captions: list):
    group_name = get_group_name(callback_data.category)
    sel = '<b>Выбрано:</b>\n' + '\n'.join(list_captions) if list_captions else 'Выбери подкатегорию для запроса цен'
    await callback.message.edit_text(
        text=sel,
        reply_markup=subgroups_keyboard(callback_data.category))


# Обрабатываем нажатие кнопок подкатегорий
@router.callback_query(MenuCD.filter(F.level == '1'))
async def process_subcategory_button_press(callback: CallbackQuery, callback_data: MenuCD, list_callbackcodes: list, list_captions: list, list_urls: list):
    if callback.data not in list_callbackcodes:
        list_callbackcodes.append(callback.data)
        list_captions.append(get_attr(callback_data.category, callback_data.subcategory, 'caption'))
        list_urls.append(get_attr(callback_data.category, callback_data.subcategory, 'url_path'))
        with open(r'files/selected_urls.pickle', 'wb') as f:
            pickle.dump(list_urls, file=f)
        sel = '<b>Выбрано:</b>\n' + '\n'.join(list_captions) if list_captions else 'Выбери подкатегорию для запроса цен'
        await callback.message.edit_text(
            text=sel,
            reply_markup=callback.message.reply_markup)
    else:
        await callback.answer('')


# Обрабатываем нажатие кнопок удаления из списка
@router.callback_query(MenuCD.filter(F.level == '2'))
async def process_delete_button_press(callback: CallbackQuery, callback_data: MenuCD, list_callbackcodes: list, list_captions: list, list_urls: list):
    item_index = int(callback_data.subcategory)
    list_callbackcodes.pop(item_index)
    list_captions.pop(item_index)
    list_urls.pop(item_index)
    if list_captions:
        with open(r'files/selected_urls.pickle', 'wb') as f:
            pickle.dump(list_urls, file=f)
        sel = '<b>Выбрано:</b>\n' + '\n'.join(list_captions)
        await callback.message.edit_text(
            text=sel,
            reply_markup=edit_keyboard(list_callbackcodes, list_captions))
    else:
        await callback.message.edit_text(
            text='КАТАЛОГ',
            reply_markup=groups_keyboard(CATALOG))


@router.callback_query(Text(text=['TO_BACK']))
async def process_back_button_press(callback: CallbackQuery, list_captions: list, kb_msg_id: list):
    sel = '<b>Выбрано:</b>\n' + '\n'.join(list_captions) if list_captions else 'КАТАЛОГ:'
    kb_msg_id.clear()
    kb_msg_id.append(await callback.message.edit_text(
        text=sel,
        reply_markup=groups_keyboard(CATALOG)))


@router.callback_query(Text(text=['EDIT']))
async def process_edit_button_press(callback: CallbackQuery, list_callbackcodes: list, list_captions: list):
    if list_captions:
        sel = '<b>Выбрано:</b>\n' + '\n'.join(list_captions)
        await callback.message.edit_text(
            text=sel,
            reply_markup=edit_keyboard(list_callbackcodes, list_captions))
    else:
        await callback.answer()


@router.callback_query(Text(text=['CANCEL']))
async def process_edit_button_press(callback: CallbackQuery, list_callbackcodes: list, list_captions: list, list_urls: list):
    list_callbackcodes.clear()
    list_captions.clear()
    list_urls.clear()
    await callback.message.edit_reply_markup()
    await callback.message.answer('Для нового запроса цен нажми /nevatom')


@router.callback_query(Text(text=['START']))
async def process_start_button_press(callback: CallbackQuery, list_captions: list):
    if list_captions:
        with open('files/selected_urls.pickle', 'rb') as fil:
            url_list = pickle.load(fil)

        await callback.message.edit_reply_markup()
        t1 = datetime.now(tz=ZoneInfo('Asia/Vladivostok'))
        await callback.message.answer(f'Старт запроса цен {t1.strftime("%H:%M:%S %d.%m.%Y")}')

        logger.info(f'{callback.from_user.id} - Запуск запроса на парсинг')
        filename = await parsing_nevatom.start_parcing(url_list)
        logger.info(f'{callback.from_user.id} - Запрос на парсинг выполнен')

        file = FSInputFile(f'files/{filename}.xlsx', filename=f'{filename} {t1.strftime("%H-%M-%S %d-%m-%Y")}.xlsx')
        logger.info(f'{callback.from_user.id} - Итоговый файл направлен в чат')
        t2 = datetime.now(tz=ZoneInfo('Asia/Vladivostok'))
        delta = t2 - t1
        await callback.message.answer(f'Запрос завершен за {delta.seconds} сек.')
        await callback.message.answer_document(file, caption='Вот фаш файл')
        await callback.message.answer(f'Для нового запроса цен нажми /nevatom')
    else:
        await callback.answer('Список для запроса цен пока пустой. Добавь в него подкатегории.')


@router.message()
async def start_handler1(msg: Message, *args, **kwargs):
    logger.info(f'{msg.from_user.id} - Пришел текст: {msg.text}')
    # pprint.pprint(kwargs, indent=4)
    await msg.reply("Текст принят. Воспрользуйтесь командой /start")
