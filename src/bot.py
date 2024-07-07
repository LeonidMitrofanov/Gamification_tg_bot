import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import Config

# Logging
logging.basicConfig(level=Config.LOG_LEVEL,
                    format='%(levelname)s | %(name)s | %(message)s | %(asctime)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[
                        logging.FileHandler(Config.LOG_FILE),
                        logging.StreamHandler()
                    ])
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
