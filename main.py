from data.loader import bot
from database.functions import (
    create_users_table,
    create_translations_table
)
import handlers

create_users_table()
create_translations_table()

bot.polling(none_stop=True)
