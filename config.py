from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('TLG_TOKEN')
# CHAT_ID = os.getenv('TLG_CHAT_ID')
APP_HOST = os.getenv('APP_HOST')
APP_PORT = os.getenv('APP_PORT')
