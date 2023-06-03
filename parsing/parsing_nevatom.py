import pprint

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import time
import random
from models.data_structure import Group, Subgroup
from pathlib import Path
from transliterate import translit
import logging, pickle

logger = logging.getLogger('logs.parsing')

DOMAIN_URL = 'https://www.nevatom.ru'
CATALOG_URL = 'https://www.nevatom.ru/catalog/'

GROUP = ''
SUBGROUP = ''
FILTER = ''
PARAMS = {'PAGEN_1': 1, 'limit': 96}
MENU_DICT = {}
TEMP_MENU_LIST = []
FULL_LIST = []
START_TIME = ''


def get_catalog():
    TEMP_MENU_LIST.clear()
    try:
        res = requests.get(CATALOG_URL)
        logger.info('Каталог запрошен')
    except Exception as ex:
        print(ex)
        logger.error(ex)
        return None

    soup = BeautifulSoup(res.text, 'html.parser')
    catalog_groups = soup.find_all('li', {'class': 'category-front__item'})
    get_subgroups(catalog_groups)

    import pickle
    with open(r'files/nevatom_catalog.pickle', 'wb') as f:
        pickle.dump(TEMP_MENU_LIST, file=f)

    return True

    # with open(r'nevatom_catalog.json', 'w') as f:
    #     json.dump(TEMP_MENU_LIST, file=f)
    #     f = json.dump(TEMP_MENU_LIST)


def get_subgroups(groups: list):
    for n, group in enumerate(groups):
        one_group = group.find('a', {'class': 'category-item__link'})
        group_item = Group()
        group_item.caption = one_group.text
        group_item.url_path = one_group['href']
        group_item.caption_translit = Path(one_group['href']).parts[-1]
        group_item.id = n

        subgroups = group.findAll('li', {'class': 'category-item__menu-item'})
        lst = []
        for m, i in enumerate(subgroups):
            i = i.find('a')
            ittem = Subgroup()
            ittem.caption = i.text.strip()
            ittem.caption_translit = Path(i['href']).parts[-1]
            ittem.url_path = i['href']
            ittem.id = m
            lst.append(ittem)
        group_item.subgroups = lst
        TEMP_MENU_LIST.append(group_item)


def get_link_to_filter_page(subgroups: list):
    global SUBGROUP
    for subgroup in subgroups:
        SUBGROUP = subgroup.text
        print(translit('...' + SUBGROUP, reversed=True, language_code='ru'))
        href = subgroup.find('a')['href']
        get_filters(DOMAIN_URL + href)


async def start_parcing(selected_subcats: list[str]):
    global GROUP, SUBGROUP
    # GROUP, SUBGROUP = group_name, subgr_name
    # START_TIME = start_time.strftime("%H:%M:%S %d-%m-%Y")
    for item in selected_subcats:
        fullurl = DOMAIN_URL + item
        print(fullurl)
        await get_filters(fullurl)
    print(translit('Все!', reversed=True, language_code='ru'))
    df = pd.DataFrame(FULL_LIST, columns=["Фильтр", "Товар", "Артикул", "Цена"])
    name_path = 'files/Nevatom.xlsx'
    df.to_excel(name_path, index=False)
    FULL_LIST.clear()
    return 'Nevatom'


async def get_filters(href):
    time.sleep(2 + random.randrange(0, 4000)/1000)
    res = requests.get(href, params=PARAMS)
    soup = BeautifulSoup(res.text, 'html.parser')
    filters = soup.find_all('div', {'class': 'filter-category__item-title'})
    await get_first_page(filters)


async def get_first_page(filters: list):
    global FILTER
    for filter_ in filters:
        FILTER = filter_.text.strip()
        print(translit('......' + FILTER, reversed=True, language_code='ru'))
        # with open('links.txt', 'a') as fil:
        #     fil.write(FILTER + '\n')
        filter_href = DOMAIN_URL + filter_.find('a')['href']
        res = requests.get(filter_href, params=PARAMS)
        await get_products(res.text, filter_href)


async def get_products(page_text: str, filter_href: str):
    soup = BeautifulSoup(page_text, 'html.parser')
    count_pages_text = soup.find('span', {'class': 'pagination-box__count'}).text
    count_pages = int(re.search(r'\d+', count_pages_text).group())
    for page_num in range(1, count_pages+1):
        print(f'.........page: {page_num}')
        if page_num > 1:
            PARAMS['PAGEN_1'] = page_num
            res = requests.get(filter_href, params=PARAMS)
            soup = BeautifulSoup(res.text, 'html.parser')

        catalog_area = soup.find('div', {'class': 'goods-series__catalog'})
        product_list = catalog_area.find_all('div', {'class': "catalog-item__body"})
        for product in product_list:
            fields = product.text.split('\n')

            title = fields[1].strip()
            product_code = re.search(r'\d+-\d+', fields[2]).group()
            price = float(re.search(r'\d+', fields[6].replace(' ', '')).group())

            lst = (FILTER, title, product_code, price)
            FULL_LIST.append(lst)
    # df = pd.DataFrame(FULL_LIST, columns=['Группа', "Погруппа", "Фильтр", "Товар", "Артикул", "Цена"])
    # df.to_excel('123.xlsx', index_label=False)

    PARAMS['PAGEN_1'] = 1


def main():
    get_catalog(True)


def main2():
    lst = [
        'asd',
        'fds'
    ]
    make_request(lst)
    df = pd.DataFrame(FULL_LIST, columns=["Фильтр", "Товар", "Артикул", "Цена"])
    df.to_excel('1234.xlsx', index_label=False)


if __name__ == '__main__':
    # with open('links.txt', 'w') as fil:
    #     fil.write('')
    # main2()
    # get_catalog()
    with open('../files/nevatom_catalog.pickle', 'rb') as fil:
        obj = pickle.load(fil)
    pprint.pprint(obj, indent=4)
