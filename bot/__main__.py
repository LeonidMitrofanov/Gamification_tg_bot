import asyncio
import logging

from bot import loader

logger = logging.getLogger(__name__)


async def main():
    try:
        await loader.loading_data()
        logger.info("Starting bot")
        await loader.dp.start_polling(loader.bot)

    except Exception as e:
        logger.exception(f"Error starting bot: {e}")
    finally:
        await loader.bot.session.close()
        logger.info("Bot stopped")


if __name__ == '__main__':
    asyncio.run(main())
