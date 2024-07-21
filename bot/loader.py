import logging
from bot.utils.logger import configurate_logger
from aiogram import Bot, Dispatcher

from services import database as db
from config import Config

# Logging configuration
configurate_logger(Config.LOG_FILE, Config.LOG_TO_FILE, Config.LOG_TO_CONSOLE, Config.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Bot and Dispatcher initialization
bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()

# Initialize the database
db.initialize(Config.DB_PATH)

# # Register handlers
# user.register_handlers_user(dp)
