import asyncio
from loader import logger, bot, db, dp


async def main():
    logger.info("Starting bot")
    # await db.add_user(1, "Лёня Митрофанов", 1, 2)  # TODO: KILLME
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(f"Error starting bot: {e}")
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
