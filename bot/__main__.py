import asyncio

import handlers
from loader import logger, bot, dp, db, load_users_from_file, Config


async def main():
    logger.info("Starting bot")
    try:
        if Config.LOAD_USERS_FROM_FILE:
            await load_users_from_file(Config.LIST_USERS_PATH)
        await dp.start_polling(bot)

    except Exception as e:
        logger.exception(f"Error starting bot: {e}")
    finally:
        await bot.session.close()
        logger.info("Bot stopped")


if __name__ == '__main__':
    asyncio.run(main())
