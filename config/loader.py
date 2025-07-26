from config.bot_config import BotConfig
from config.db_config import DbConfig

from dataclasses import dataclass

@dataclass
class Config:
    bot: BotConfig
    db: DbConfig


def load_config() -> Config:
    bot_config = BotConfig.from_env()
    db_config = DbConfig.from_env()

    return Config(
        bot=bot_config,
        db=db_config
    )


app_config = load_config()
