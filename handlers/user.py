from data.loader import bot, translator
from data.utils import send_translations_history
from telebot.types import Message, ReplyKeyboardRemove, CallbackQuery
from keyboards.reply import show_start_kb, show_langs_reply_kb
from keyboards.inline import delete_translation_kb
from database.functions import add_user, get_user_translations, add_translation, delete_translation
from googletrans import LANGUAGES, LANGCODES


@bot.message_handler(commands=['start'])
def handle_command_start(message: Message):
    chat_id = message.chat.id
    add_user(chat_id, message.from_user.username)
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

    # отправка истории переводов
    send_translations_history(
        bot=bot, translations=translations, chat_id=chat_id,
    )


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


@bot.callback_query_handler(func=lambda call: call.data.startswith('delete'))
def delete_translation_(call: CallbackQuery):
    print(call.data)
    translation_id = int(call.data.split(':')[-1])
    delete_translation(translation_id)
    bot.delete_message(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id
    )