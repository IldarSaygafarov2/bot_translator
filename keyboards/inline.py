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


def delete_translation_kb(translation_id, chat_id=None):
    kb = InlineKeyboardMarkup()
    callback_data = f'delete:{translation_id}' if chat_id is None else f'delete:{translation_id}:{chat_id}'
    kb.add(InlineKeyboardButton(text='Удалить', callback_data=callback_data))
    return kb


def show_users_kb(users):
    kb = InlineKeyboardMarkup(row_width=1)
    result = []
    for chat_id, username in users:
        result.append(
            InlineKeyboardButton(text=username, callback_data=f'user:{chat_id}')
        )
    kb.add(*result)
    return kb

