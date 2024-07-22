import asyncio

from bot.loader import logger, bot, dp, loading_data


async def main():
    logger.info("Starting bot")
    try:
        await loading_data()
        await dp.start_polling(bot)

    except Exception as e:
        logger.exception(f"Error starting bot: {e}")
    finally:
        await bot.session.close()
        logger.info("Bot stopped")


if __name__ == '__main__':
    asyncio.run(main())
