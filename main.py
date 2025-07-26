from data.loader import bot, translator
from telebot.types import Message, CallbackQuery, ReplyKeyboardRemove
from keyboards.reply import show_start_kb, show_langs_reply_kb
from keyboards.inline import show_langs_kb
from googletrans import LANGUAGES, LANGCODES
from database.functions import (
    create_users_table,
    create_translations_table,
    add_user,
    add_translation,
    get_user_translations
)


create_users_table()
create_translations_table()


# /start, /help
@bot.message_handler(commands=['start'])
def handle_command_start(message: Message):
    chat_id = message.chat.id
    add_user(chat_id)
    bot.send_message(chat_id, f'Hello, {message.from_user.first_name}', 
                     reply_markup=show_start_kb())


# Перевод
@bot.message_handler(func=lambda msg: msg.text == 'Перевод')
def start_translation(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Выберите язык, с которого хотите сделать перервод', reply_markup=show_langs_reply_kb())


@bot.message_handler(func=lambda msg: msg.text == 'История переводов')
def show_translation_history(message: Message):
    chat_id = message.chat.id
    translations = get_user_translations(chat_id)
    if not translations:
        return bot.send_message(chat_id, "История пуста")

    for _id, lang_from, lang_to, original, translated, _ in translations:
        msg = f'''
FROM: <i>{lang_from}</i>
TO: <i>{lang_to}</i>
ORIGINAL: <i>{original}</i>
TRANSLATED: <i>{translated}</i>
'''
        bot.send_message(chat_id, msg)


    bot.send_message(chat_id, 'Ваша история переводов')


@bot.message_handler(func=lambda msg: msg.text in LANGUAGES.values())
def get_lang_from(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Выберите язык, на который хотите сделать перевод',reply_markup=show_langs_reply_kb())
    bot.register_next_step_handler(message, get_lang_to, message.text)


def get_lang_to(message: Message, lang_from: str):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Напишите слово или текст для перевода", reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, translate, lang_from, message.text)


def translate(message: Message, lang_from: str, lang_to: str):
    print(message.text, lang_from, lang_to)
    code_from = LANGCODES[lang_from]
    code_to = LANGCODES[lang_to]
    chat_id = message.chat.id

    translated = translator.translate(message.text, code_to, code_from).text

    msg = f'''
FROM: <i>{lang_from}</i>
TO: <i>{lang_to}</i>
ORIGINAL: <i>{message.text}</i>
TRANSLATED: <i>{translated}</i>
'''

    add_translation(code_from, code_to, message.text, translated, chat_id)
    bot.send_message(chat_id, msg, reply_markup=show_start_kb())
    

# @bot.callback_query_handler()
# def get_lang_from(call: CallbackQuery):
#     print(call.data)

#
# @bot.callback_query_handler(func=lambda call: call.data.startswith('next_page'))
# def show_next_page(call: CallbackQuery):
#     _, page, start, finish, total_pages = call.data.split(':')
#
#     if int(page) == int(total_pages):
#         return bot.answer_callback_query(
#             callback_query_id=call.id,
#             text='Вы уже на последней странице',
#             show_alert=True
#         )
#
#     bot.edit_message_reply_markup(
#         message_id=call.message.message_id,
#         chat_id=call.message.chat.id,
#         reply_markup=show_langs_kb(
#             page=int(page)+1,
#             start=int(start)+9,
#             finish=int(finish)+9
#         )
#     )


bot.polling(none_stop=True)
