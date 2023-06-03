from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from models.data_structure import Group
import pickle
import logging
from aiogram.filters.callback_data import CallbackData

logger = logging.getLogger('logs.inline_keyboards')


class MenuCD(CallbackData, prefix='my_callback'):
    level: str
    category: int
    subcategory: int


class AnyUsersList(CallbackData, prefix='anyuser'):
    id: int
    is_user_list: bool


def make_callback_data(level, category=0, subcategory=0):
    return MenuCD(level=level, category=category, subcategory=subcategory).pack()


def groups_keyboard(lst: list[Group]) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 0
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    for i in lst:
        buttons.append(InlineKeyboardButton(text=i.caption,
                                            callback_data=make_callback_data(CURRENT_LEVEL,
                                                                             i.id)))
    kb_builder.row(*buttons, width=2)

    kb_builder.row(InlineKeyboardButton(text='💬 РЕДАКТИРОВАТЬ СПИСОК...', callback_data='EDIT'))


    kb_builder.row(InlineKeyboardButton(text='⭕ ОТМЕНА', callback_data='CANCEL'),
                   InlineKeyboardButton(text='🚀 ЗАПУСК', callback_data='START'))

    return kb_builder.as_markup()


def subgroups_keyboard(category: int) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 1
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    with open('files/nevatom_catalog.pickle', 'rb') as fil:
        obj = pickle.load(fil)

    chosen_subgroup = list(filter(lambda x: x.id == category, obj))[0]

    for i in chosen_subgroup.subgroups:
        buttons.append(InlineKeyboardButton(text=i.caption,
                                            callback_data=make_callback_data(CURRENT_LEVEL,
                                                                             category,
                                                                             i.id)))
    kb_builder.row(*buttons, width=2)
    kb_builder.row(InlineKeyboardButton(text='💬 РЕДАКТИРОВАТЬ СПИСОК...', callback_data='EDIT'))
    logger.debug('Клавиатура с подгруппами готова 1')
    kb_builder.row(InlineKeyboardButton(text='⬅️ НАЗАД', callback_data='TO_BACK'))
    logger.debug('Клавиатура с подгруппами готова 2')
    return kb_builder.as_markup()


def edit_keyboard(cbd: list, selected_list: list) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 2
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    for n, i in enumerate(selected_list):
        buttons.append(InlineKeyboardButton(text='✖️ ' + i,
                                            callback_data=make_callback_data(CURRENT_LEVEL, 0, n)))

    kb_builder.row(*buttons, width=1)
    logger.debug('Клавиатура с удаленными готова 1')

    kb_builder.row(InlineKeyboardButton(
                text='⬅️ НАЗАД',
                callback_data='TO_BACK'))

    logger.debug('Клавиатура с удаленными готова 2')

    return kb_builder.as_markup()


def yesno_keyboard() -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    kb_builder.row(
        InlineKeyboardButton(
            text='⭕ ОТМЕНА',
            callback_data='YES'),
        InlineKeyboardButton(
            text='✅ ДА',
            callback_data='NO')
    )

    return kb_builder.as_markup()


def any_users_keyboard(any_user_list: list, is_user_list: bool):
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    for n, i in enumerate(any_user_list):
        buttons.append(InlineKeyboardButton(text='✖️ ' + str(i),
                                            callback_data=AnyUsersList(id=i, is_user_list=is_user_list).pack()))

    kb_builder.row(*buttons, width=1)
    kb_builder.row(InlineKeyboardButton(
        text='⭕ ОТМЕНА',
        callback_data='CANCEL'))

    return kb_builder.as_markup()
