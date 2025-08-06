from keyboards.inline import delete_translation_kb
from database.functions import get_user_chat_id


def send_translations_history(bot, translations, chat_id, is_for_admin=False):
    if not translations:
        return bot.send_message(chat_id, "История пуста")

    for _id, lang_from, lang_to, original, translated, user_id in translations:
        user_chat_id = get_user_chat_id(user_id)

        msg = f'''
FROM: <i>{lang_from}</i>
TO: <i>{lang_to}</i>
ORIGINAL: <i>{original}</i>
TRANSLATED: <i>{translated}</i>
'''
        if not is_for_admin:
            bot.send_message(chat_id, msg, reply_markup=delete_translation_kb(_id))
        else:
            bot.send_message(chat_id, msg, reply_markup=delete_translation_kb(_id, chat_id=user_chat_id))

