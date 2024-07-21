import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()


@dataclass
class Config:
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', "INFO")
    LOG_FILE: str = os.getenv('LOG_FILE', 'bot.log')
    LOG_TO_FILE: bool = os.getenv('LOG_TO_FILE', 'True') == 'True'
    LOG_TO_CONSOLE: bool = os.getenv('LOG_TO_CONSOLE', 'True') == 'True'
    DB_PATH: str = os.getenv('DB_PATH', 'database.db')
    SUPERUSER_IDS = list(map(int, str(os.getenv('SUPERUSER_IDS')).split(' ')))
