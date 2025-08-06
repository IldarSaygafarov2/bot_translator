from telebot.types import Message, CallbackQuery

from config.loader import app_config
from data.loader import bot
from data.utils import send_translations_history
from database.functions import get_all_users, get_user_translations, delete_translation
from keyboards.inline import show_users_kb
from keyboards.reply import show_admin_start_kb


def is_admin(msg: Message | CallbackQuery):
    if isinstance(msg, Message):
        return msg.chat.id in app_config.bot.admins_chat_ids
    elif isinstance(msg, CallbackQuery):
        return msg.message.chat.id in app_config.bot.admins_chat_ids


@bot.message_handler(func=lambda msg: is_admin(msg), commands=['start'])
def admin_start(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Привет, админ", reply_markup=show_admin_start_kb())


@bot.message_handler(
    func=lambda msg: is_admin(msg) and msg.text == 'Пользователи'
)
def show_users_to_admin(message: Message):
    chat_id = message.chat.id
    users = get_all_users()
    print(users)
    bot.send_message(chat_id, "Все пользователи", reply_markup=show_users_kb(users))


@bot.callback_query_handler(
    func=lambda call: is_admin(call) and call.data.startswith('user')
)
def get_user_translations_for_admin(call: CallbackQuery):
    chat_id = int(call.data.split(':')[-1])
    user_translations = get_user_translations(chat_id)
    admin_chat_id = call.message.chat.id

    send_translations_history(bot=bot, translations=user_translations, chat_id=admin_chat_id, is_for_admin=True)


@bot.callback_query_handler(
    func=lambda call: is_admin(call) and call.data.startswith('delete')
)
def delete_user_translation_by_admin(call: CallbackQuery):
    _, translation_id, user_chat_id = call.data.split(':')
    admin_chat_id = call.message.chat.id

    bot.send_message(admin_chat_id, "Напишите причину удаления данного перевода")
    bot.register_next_step_handler(call.message, notify_and_delete, translation_id, user_chat_id)


def notify_and_delete(message: Message, translation_id, user_chat_id):
    print(message.text, translation_id, user_chat_id)
    translation_id, user_chat_id = int(translation_id), int(user_chat_id)

    delete_translation(translation_id)
    bot.send_message(user_chat_id, message.text)
    bot.send_message(message.chat.id, "Перевод удален и пользователь оповещён об этом")


# git add .
# git commit -m "message"
# git push