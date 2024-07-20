import logging
from aiogram import Bot, Dispatcher

from services import database as db
from config import Config
from handlers import user


# Logging configuration
class FlushFileHandler(logging.FileHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()


log_handlers = [logging.StreamHandler()]
if Config.LOG_TO_FILE:
    log_handlers.append(FlushFileHandler(Config.LOG_FILE))

logging.basicConfig(level=Config.LOG_LEVEL,
                    format='%(asctime)s\t %(levelname)s\t %(name)s\t %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=log_handlers)

logger = logging.getLogger(__name__)

# Bot and Dispatcher initialization
bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()

# Initialize the database
db.initialize(Config.DB_PATH)

# # Register handlers
# user.register_handlers_user(dp)
