from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from data_structure import Group, Subgroup
import pickle

from aiogram.filters.callback_data import CallbackData


with open('archives/data.pickle', 'rb') as fil:
    obj = pickle.load(fil)


class MenuCD(CallbackData, prefix='my_callback'):
    level: str
    category: int
    subcategory: int


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

    chosen_subgroup = list(filter(lambda x: x.id == category, obj))[0]

    for i in chosen_subgroup.subgroups:
        buttons.append(InlineKeyboardButton(text=i.caption,
                                            callback_data=make_callback_data(CURRENT_LEVEL,
                                                                             category,
                                                                             i.id)))
    kb_builder.row(*buttons, width=2)
    kb_builder.row(InlineKeyboardButton(text='💬 РЕДАКТИРОВАТЬ СПИСОК...', callback_data='EDIT'))
    kb_builder.row(InlineKeyboardButton(text='⬅️ НАЗАД', callback_data='TO_BACK'))

    return kb_builder.as_markup()


def edit_keyboard(cbd: list, selected_list: list) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 2
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    for n, i in enumerate(selected_list):
        buttons.append(InlineKeyboardButton(text='❌ ' + i,
                                            callback_data=make_callback_data(CURRENT_LEVEL, 0, n)))

    kb_builder.row(*buttons, width=1)
    kb_builder.row(InlineKeyboardButton(
            text='⬅️ НАЗАД',
            callback_data='TO_BACK'))

    return kb_builder.as_markup()
