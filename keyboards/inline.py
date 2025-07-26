from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from googletrans import LANGUAGES


def show_langs_kb(page: int = 1, start: int = 0, finish: int = 9):
    kb = InlineKeyboardMarkup()
    total_pages = round(len(LANGUAGES)/9)
    buttons = []
    for lang_code, lang in list(LANGUAGES.items())[start: finish]:
        buttons.append(
            InlineKeyboardButton(text=lang, callback_data=f'lang:{lang_code}')
        )
    kb.add(*buttons)
    kb.row(
        InlineKeyboardButton('<', callback_data=f'prev:{page}:{start}:{finish}'),
        InlineKeyboardButton(f'{page}/{total_pages}', callback_data='page'),
        InlineKeyboardButton('>', callback_data=f'next:{page}:{start}:{finish}:{total_pages}')
    )
    return kb
