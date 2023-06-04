from dotenv import load_dotenv
import os
import logging

load_dotenv()

TOKEN = os.getenv('TLG_TOKEN')
TOKEN2 = os.getenv('TLG_TOKEN2')
APP_HOST = os.getenv('APP_HOST')
APP_PORT = os.getenv('APP_PORT')

DEVELOP = True

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('logs/main.log', mode='w')
    fh.setLevel(logging.DEBUG)
    fmtstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    fmtdate = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(fmtstr, fmtdate)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
