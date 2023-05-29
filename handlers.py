from aiogram import F, Router, html, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile, InputFile
from aiogram.filters import Command, CommandObject, Text
from datetime import datetime
from keyboards import groups_keyboard, subgroups_keyboard, MenuCD, edit_keyboard
import pprint, json
import pickle
from pathlib import Path



router = Router()

msg_content = {
    'phone_number': "Телефон",
    'email': 'Электропочта',
    'mention': "Имярек",
    "hashtag": "Хэштег",
    'bot_command': "Команда",
    'url': "Урл :)",
    'bold': "Жирный",
    'italic': "Виталик",
    'underline': 'Подчерк'
}

with open('data.pickle', 'rb') as fil:
    obj = pickle.load(fil)


def get_group_attr(category: int):
    return list(filter(lambda y: y.id == category, obj))[0].caption


def get_attr(category: int, subcategory: int, param: str):
    a = list(filter(lambda x: x.id == category, obj))[0].subgroups
    b = list(filter(lambda y: y.id == subcategory, a))[0]
    dic_ = {'caption': b.__getattribute__('caption'),
            'caption_translit': b.__getattribute__('caption_translit'),
            'url_path': b.__getattribute__('url_path'),
            # 'subgroups': b.__getattribute__('subgroups')
            }
    return dic_[param]


@router.message(Command("start"))
async def start_handler1(msg: Message, *args, **kwargs):
    await msg.answer("Привет! Это служебный бот.\n"
                     "Команды:\n"
                     "/help - список команд (в разработке)\n"
                     "/nevatom - запуск запроса цен на сайте Nevatom"
                     )
    # await msg.answer()


@router.message(Command("nevatom"))
async def start_handler2(msg: Message, mylist: list, mylist2: list, mylist3: list, group_name: str):
    mylist.clear()
    mylist2.clear()
    mylist3.clear()
    await msg.answer("Для сбора информации о ценах с сайта Nevatom нужно выбрать интересующие подкатегории. "
                     "Для этого нажать на нужный раздел каталога ниже, после чего нажать на нужную подкатегорию.  "
                     "Она добавится в список на запрос цен.\n"
                     "Вернуться к разделам можно по кнопке '⬅️ НАЗАД В КАТАЛОГ'.\n"
                     "Выбери таким образом все нужные подкатегории и запусти запрос из каталога по кнопке '🚀 ЗАПУСТИТЬ ПОИСК'.\n"
                     "Удалить из списка лишнее можно по кнопке '💬 РЕДАКТИРОВАТЬ ВЫБРАННОЕ'")
    await msg.answer("КАТАЛОГ:",
                     reply_markup=groups_keyboard(obj))


# Обрабатываем нажатие кнопок каталога
@router.callback_query(MenuCD.filter(F.level == '0'))
async def process_catalog_button_press(callback: CallbackQuery, callback_data: MenuCD, mylist2: list, group_name:str, *args, **kwargs):
    group_name = get_group_attr(callback_data.category)
    sel = '<b>Выбрано:</b>\n' + '\n'.join(mylist2) if mylist2 else 'Выберите подкатегорию для запроса цен'
    await callback.message.edit_text(
        text=sel,
        # text=sel + '\n\nПОДКАТЕГОРИИ:',
        reply_markup=subgroups_keyboard(callback_data.category))


@router.callback_query(MenuCD.filter(F.level == '1'))
async def process_subcategory_button_press(callback: CallbackQuery, callback_data: MenuCD, mylist: list, mylist2: list, mylist3: list, subgr_name: str):
    subgr_name = get_attr(callback_data.category, callback_data.subcategory, 'caption')
    if callback.data not in mylist:
        mylist.append(callback.data)
        mylist2.append(get_attr(callback_data.category, callback_data.subcategory, 'caption'))
        mylist3.append(get_attr(callback_data.category, callback_data.subcategory, 'url_path'))
        with open(r'url_list.pickle', 'wb') as f:
            pickle.dump(mylist3, file=f)
        sel = '<b>Выбрано:</b>\n' + '\n'.join(mylist2) if mylist2 else 'Выберите подкатегорию для запроса цен'
        await callback.message.edit_text(
            # text=sel + '\n\nПОДКАТЕГОРИИ:',
            text=sel,
            reply_markup=callback.message.reply_markup)
    else:
        await callback.answer('')


@router.callback_query(MenuCD.filter(F.level == '2'))
async def process_subcategory_button_press(callback: CallbackQuery, callback_data: MenuCD, mylist: list, mylist2: list, mylist3: list, *args, **kwargs):
    print(callback.data)
    item_index = int(callback_data.subcategory)
    mylist.pop(item_index)
    mylist2.pop(item_index)
    mylist3.pop(item_index)
    print(mylist2)
    if mylist2:
        with open(r'url_list.pickle', 'wb') as f:
            pickle.dump(mylist3, file=f)
        sel = '<b>Выбрано:</b>\n' + '\n'.join(mylist2)
        await callback.message.edit_text(
            text=sel,
            reply_markup=edit_keyboard(mylist, mylist2))
    else:
        await callback.message.edit_text(
            text='КАТАЛОГ:',
            reply_markup=groups_keyboard(obj))
    # print(mylist)
    # print(mylist.index(callback.data))
    # subgr_name = get_attr(callback_data.category, callback_data.subcategory, 'caption')
    # if callback.data not in mylist:
    #     mylist.append(callback.data)
    #     mylist2.append(get_attr(callback_data.category, callback_data.subcategory, 'caption'))
    #     mylist3.append(get_attr(callback_data.category, callback_data.subcategory, 'url_path'))
    #     with open(r'url_list.pickle', 'wb') as f:
    #         pickle.dump(mylist3, file=f)
    #     sel = '<b>Выбрано:</b>\n' + '\n'.join(mylist2) if mylist2 else 'Выберите подкатегорию для запроса цен'
    #     await callback.message.edit_text(
    #         # text=sel + '\n\nПОДКАТЕГОРИИ:',
    #         text=sel,
    #         reply_markup=callback.message.reply_markup)
    # else:
    #     await callback.answer('')


@router.callback_query(Text(text=['TO_BACK']))
async def process_back_button_press(callback: CallbackQuery, mylist2: list, *args, **kwargs):
    sel = '<b>Выбрано:</b>\n' + '\n'.join(mylist2) if mylist2 else 'Выберите подкатегорию для запроса цен'
    await callback.message.edit_text(
        # text=sel + '\n\nКАТАЛОГ:',
        text=sel,
        reply_markup=groups_keyboard(obj))


@router.callback_query(Text(text=['EDIT']))
async def process_back_button_press(callback: CallbackQuery, mylist: list, mylist2: list, *args, **kwargs):
    if mylist2:
        sel = '<b>Выбрано:</b>\n' + '\n'.join(mylist2)
        await callback.message.edit_text(
            text=sel,
            reply_markup=edit_keyboard(mylist, mylist2))
    else:
        await callback.answer()


@router.callback_query(Text(text=['START']))
async def process_start_button_press(callback: CallbackQuery, mylist: list, mylist2: list, mylist3, group_name: str, subgr_name: str):
    if mylist2:
        from search.search import make_request
        with open('url_list.pickle', 'rb') as fil:
            obj = pickle.load(fil)

        await callback.message.edit_reply_markup()
        t1 = datetime.now()
        await callback.message.answer(f'Старт запроса цен {t1.strftime("%H:%M:%S %d.%m.%Y")}')
        filename = await make_request(obj, group_name, subgr_name)
        file = FSInputFile(filename + '.xlsx', filename=f'{filename} {t1.strftime("%H-%M-%S %d-%m-%Y")}.xlsx')
        t2 = datetime.now()
        delta = t2 - t1
        await callback.message.answer(f'Запрос завершен за {delta.seconds} сек.')
        await callback.message.answer_document(file, caption='Вот фаш файл')
        # mylist.clear()
        # mylist2.clear()
        # mylist3.clear()
        await callback.message.answer(f'Для нового запроса цен нажмите /nevatom')
    else:
        await callback.answer('Список для запроса цен пока пустой. Добавьте в него подкатегории.')


