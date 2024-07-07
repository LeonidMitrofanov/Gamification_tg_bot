import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import Config

# Logging configuration
class FlushFileHandler(logging.FileHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()

handlers = [logging.StreamHandler()]
if Config.LOG_TO_FILE:
    handlers.append(FlushFileHandler(Config.LOG_FILE))

logging.basicConfig(level=Config.LOG_LEVEL,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=handlers)

logger = logging.getLogger(__name__)

# Bot and Dispatcher initialization
bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()


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
