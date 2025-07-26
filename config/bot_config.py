import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class BotConfig:
    token: str

    @staticmethod
    def from_env() -> 'BotConfig':
        return BotConfig(
            token=os.getenv('BOT_TOKEN')
        )


