import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import Config
from services.sql import DataBase as DB
from handlers import user


# Logging configuration
class FlushFileHandler(logging.FileHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()


handlers = [logging.StreamHandler()]
if Config.LOG_TO_FILE:
    handlers.append(FlushFileHandler(Config.LOG_FILE))

logging.basicConfig(level=Config.LOG_LEVEL,
                    format='%(levelname)s - %(asctime)s - %(name)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=handlers)

logger = logging.getLogger(__name__)

# Bot and Dispatcher initialization
bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()

# Initialize the database
DB()


# # Register handlers
# user.register_handlers_user(dp)

async def main():
    logger.info("Starting bot")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(f"Error starting bot: {e}")
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
