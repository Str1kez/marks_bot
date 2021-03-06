import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
session = requests.Session()
session.proxies = {
    'https': 'http://squid2.kpfu.ru:8080',
    'http': 'http://squid2.kpfu.ru:8080',
}
