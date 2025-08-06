import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class BotConfig:
    token: str
    admins_chat_ids: list

    @staticmethod
    def from_env() -> 'BotConfig':
        return BotConfig(
            token=os.getenv('BOT_TOKEN'),
            admins_chat_ids=[int(_id) for _id in os.getenv('ADMINS_CHAT_IDS').split(',') if _id]
        )


