import logging
import asyncio
from utils.logger import configurate_logger
from aiogram import Bot, Dispatcher

from services.models import *
from services import database as db
from config import Config

# Logging configuration
configurate_logger(Config.LOG_FILE, Config.LOG_TO_FILE, Config.LOG_TO_CONSOLE, Config.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Bot and Dispatcher initialization
bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()

# Initialize the database
db.initialize(Config.DB_PATH)


# # Register handlers
# user.register_handlers_user(dp)
async def load_users_from_file(file_path: str):
    logger.debug(f"load_users_from_file called with file_path: {file_path}")

    tribe_mapping = {
        "ignis": Tribe.IGNIS.value,
        "aqua": Tribe.AQUA.value,
        "air": Tribe.AIR.value,
        "terra": Tribe.TERRA.value
    }

    try:
        with open(file_path) as file:
            logger.debug(f"Opened file: {file_path}")
            users = file.read().split('\n')
            logger.debug(f"Read {len(users)} lines from file")

            for user in users:
                if user.strip() == "":
                    continue

                info = [part.strip() for part in user.split('|')]
                if len(info) != 3:
                    logger.warning(f"Skipping malformed line: {user}")
                    continue

                tg_id, name, tribe_name = int(info[0]), info[1], info[2]
                tribe_value = tribe_mapping.get(tribe_name.lower())
                logger.debug(f"Parsed user info - tg_id: {tg_id}, name: {name}, tribe_name: {tribe_name},"
                             f" tribe_value: {tribe_value}")

                if tribe_value is not None:
                    if not db.user_exists(tg_id=tg_id):
                        if tg_id in Config.SUPERUSER_IDS:
                            await db.add_admin(tg_id, name, tribe_value)
                        else:
                            await db.add_user(tg_id, name, tribe_value)
                    else:
                        logger.info(f"User already exists - tg_id: {tg_id}")
                else:
                    logger.warning(f"Tribe not found for tribe_name: {tribe_name}")

    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        exit()
    except Exception as e:
        logger.exception(f"Error loading users from file: {e}")

