import datetime as dt

from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста
EDU_LOGIN = env.str("EDU_LOGIN")
EDU_PASSWORD = env.str("EDU_PASSWORD")
NOW = dt.datetime.now()
YESTERDAY = NOW - dt.timedelta(days=4)
