from config.loader import app_config

from telebot import TeleBot
from googletrans import Translator

# pip install googletrans==4.0.0rc1


# bot object
bot = TeleBot(token=app_config.bot.token, parse_mode='HTML')

# translator object

translator = Translator()
