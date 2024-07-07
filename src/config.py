import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()
@dataclass
class Config:
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')





