import asyncio

import handlers
from loader import logger, bot, db, dp


async def main():
    logger.info("Starting bot")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(f"Error starting bot: {e}")
    finally:
        await bot.session.close()
        logger.info("Bot stopped")


if __name__ == '__main__':
    asyncio.run(main())
