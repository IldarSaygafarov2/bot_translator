from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class DbConfig:
    host: str
    user: str
    password: str
    database: str
    port: int

    @staticmethod
    def from_env() -> 'DbConfig':
        return DbConfig(
            host=os.getenv('PG_HOST'),
            password=os.getenv('PG_PASSWORD'),
            user=os.getenv('PG_USER'),
            database=os.getenv('PG_DATABASE'),
            port=int(os.getenv('PG_PORT', 5432))
        )