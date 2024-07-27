import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()


@dataclass
class Config:
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')
    LOG_LEVEL: str = "INFO"                            # You can set DEBUG for more detailed logging
    LOG_FILE: str = "bot/logs/bot.log"                  # Path to the log file
    LOG_TO_FILE: bool = True                            # Set to False if you don't want to log to a file
    LOG_TO_CONSOLE: bool = True                         # Set to False if you don't want to log to a console
    LOAD_USERS_FROM_FILE: bool = False                   # Set to False if you don't want to load users from file
    LIST_USERS_PATH: str = "bot/data/users.txt"         # Path to the list of users to load file
    DB_PATH: str = "bot/data/database.db"               # Path to the SQLite database file
    MESSAGES_PATH: str = "bot/constants/messages"       # Path to the messages to load file
    SUPERUSER_IDS = list(map(int,                       # List of superuser id's
                             os.getenv("SUPERUSER_IDS")
                             .strip().split())),
    DEFAULT_LANGUAGE: str = "ru"                        # Set default language
    REGISTRATION_BY_SECRETKEY: bool = True              # Set to False if you don't want to registrate by secret key
    USER_SECRETKEY: str = os.getenv('USER_SECRETKEY')
    ADMIN_SECRETKEY: str = os.getenv('ADMIN_SECRETKEY')
