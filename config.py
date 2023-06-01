from dotenv import load_dotenv
import os
import logging

load_dotenv()

TOKEN = os.getenv('TLG_TOKEN')
TOKEN2 = os.getenv('TLG_TOKEN2')
DEVELOP = bool(os.getenv('DEVELOP'))
APP_HOST = os.getenv('APP_HOST')
APP_PORT = os.getenv('APP_PORT')


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # создаем файловый обработчик, который
    # регистрирует отладочные сообщения
    fh = logging.FileHandler('log/main.log', mode='w')
    # fh = logging.handlers.RotatingFileHandler(
    #     'log/main.log', maxBytes=1000000, backupCount=1)
    fh.setLevel(logging.DEBUG)
    # создаем консольный обработчик
    # с более высоким уровнем журнала
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # создаем форматтер и добавляем его в обработчики
    fmtstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    fmtdate = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(fmtstr, fmtdate)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # добавляем настроенные обработчики в логгер
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger