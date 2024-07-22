import logging
from aiogram import Bot, Dispatcher

from bot.utils.logger import configurate_logger
from bot.config import Config
from bot.enums.enums import Tribe
from bot.services.database.response.base import initialize as db_initialize
from bot.services.database.response import user as db_user

from bot.telegram.handlers.admin import router as admin_router
from bot.telegram.handlers.common import router as common_router

# Logging configuration
configurate_logger(Config.LOG_FILE, Config.LOG_TO_FILE, Config.LOG_TO_CONSOLE, Config.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Bot and Dispatcher initialization
bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()

# Include routers
dp.include_routers(admin_router, common_router)


async def loading_data():
    # Initialize the database
    await db_initialize(Config.DB_PATH)

    # Load users from file
    if Config.LOAD_USERS_FROM_FILE:
        await load_users_from_file(Config.LIST_USERS_PATH)


async def load_users_from_file(file_path: str):
    logger.debug(f"load_users_from_file called with file_path: {file_path}")

    tribe_mapping = {
        "ignis": Tribe.IGNIS.value,
        "aqua": Tribe.AQUA.value,
        "air": Tribe.AIR.value,
        "terra": Tribe.TERRA.value
    }

    try:
        with open(file_path, 'r') as file:
            logger.debug(f"Opened file: {file_path}")
            users = file.read().strip().split('\n')
            logger.debug(f"Read {len(users)} lines from file")

            for user in users:
                if not user.strip():
                    continue

                info = [part.strip() for part in user.split('|')]
                if len(info) != 3:
                    logger.warning(f"Skipping malformed line: {user}")
                    continue

                try:
                    tg_id = int(info[0])
                    name = info[1]
                    tribe_name = info[2]
                except ValueError:
                    logger.warning(f"Skipping line with invalid format: {user}")
                    continue

                tribe_value = tribe_mapping.get(tribe_name.lower())
                logger.debug(f"Parsed user info - tg_id: {tg_id}, name: {name}, tribe_name: {tribe_name}, "
                             f"tribe_value: {tribe_value}")

                if tribe_value is not None:
                    if not await db_user.user_exists(tg_id=tg_id):
                        if tg_id in Config.SUPERUSER_IDS:
                            await db_user.add_admin(tg_id, name, tribe_value)
                        else:
                            await db_user.add_user(tg_id, name, tribe_value)
                    else:
                        logger.warning(f"User already exists - tg_id: {tg_id}")
                else:
                    logger.warning(f"Tribe not found for tribe_name: {tribe_name}")

    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except Exception as e:
        logger.exception(f"Error loading users from file: {e}")
