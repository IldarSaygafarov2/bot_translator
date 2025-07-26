# Перевод История переводов

from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from googletrans import LANGUAGES



def show_start_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        KeyboardButton(text='Перевод'),
        KeyboardButton(text='История переводов'),
    ]
    kb.add(*buttons)
    return kb


def show_langs_reply_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)  # row_width=3 - кол-во кнопок на линии
    buttons = []
    for lang_name in LANGUAGES.values():
        buttons.append(
            KeyboardButton(text=lang_name)
        )
    kb.add(*buttons)
    return kb