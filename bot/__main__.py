import asyncio
import logging

from bot import loader


async def main():
    try:
        await loader.loading_data()
        logger = logging.getLogger(__name__)
        logger.info("Starting bot")
        await loader.dp.start_polling(loader.bot)

    except Exception as e:
        loader.logger.exception(f"Error starting bot: {e}")
    finally:
        await loader.bot.session.close()
        loader.logger.info("Bot stopped")


if __name__ == '__main__':
    asyncio.run(main())
