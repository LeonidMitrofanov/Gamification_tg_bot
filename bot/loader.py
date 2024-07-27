import logging
from aiogram import Bot, Dispatcher

from bot.config import Config
from bot.enums import language
from bot.enums.enums import Tribe
from bot.telegram.handlers import handlers_config
from bot.telegram.handlers.admin import router as admin_router
from bot.telegram.handlers.common import router as common_router
from bot.services.database.response import user as db_user
from bot.services.database.response.base import initialize as db_initialize
from bot.utils.json_loader import load_messages_from_xml
from bot.utils.logger import configurate_logger
from bot.exceptions.loading import InvalidDefaultLanguageError

# Variables
logger: logging.Logger
bot: Bot
dp: Dispatcher


async def loading_data():
    global logger, bot, dp
    # Logging configuration
    configurate_logger(Config.LOG_FILE, Config.LOG_TO_FILE, Config.LOG_TO_CONSOLE, Config.LOG_LEVEL)
    logger = logging.getLogger(__name__)

    logger.debug("Initializing Bot and Dispatcher")
    # Bot and Dispatcher initialization
    bot = Bot(token=Config.BOT_TOKEN)
    dp = Dispatcher()

    # Include routers
    logger.debug("Including routers")
    dp.include_routers(admin_router, common_router)

    logger.debug("Set default language")
    # Set default language
    if not (Config.DEFAULT_LANGUAGE in language.Language.ALL):
        raise InvalidDefaultLanguageError(Config.DEFAULT_LANGUAGE)
    language.Language.DEFAULT = Config.DEFAULT_LANGUAGE

    # Load messages from json
    handlers_config.menu_messages = load_messages_from_xml(Config.MESSAGES_PATH + '/common/menu.xml')
    handlers_config.registration_messages = load_messages_from_xml(Config.MESSAGES_PATH + '/common/registration.xml')

    # Set secret keys
    logger.debug("Set SECRET KEYS")
    handlers_config.ADMIN_SECRETKEY = Config.ADMIN_SECRETKEY
    handlers_config.USER_SECRETKEY = Config.USER_SECRETKEY

    # Initialize the database
    await db_initialize(Config.DB_PATH)

    # Load users from file
    if Config.LOAD_USERS_FROM_FILE:
        logger.debug(f"Loading users from file: {Config.LIST_USERS_PATH}")
        await load_users_from_file(Config.LIST_USERS_PATH)
        logger.info("Users loaded from file successfully")
    else:
        logger.debug("LOAD_USERS_FROM_FILE is set to False, skipping loading users from file")

    logger.debug("loading_data function completed successfully")


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
                if len(info) < 3:
                    logger.warning(f"Skipping malformed line: {user}")
                    continue

                try:
                    tg_id = int(info[0])
                    name = info[1]
                    tribe_name = info[2]
                    locale = info[3] if len(info) > 3 else None
                except ValueError:
                    logger.warning(f"Skipping line with invalid format: {user}")
                    continue

                tribe_value = tribe_mapping.get(tribe_name.lower())
                logger.debug(f"Parsed user info - tg_id: {tg_id}, name: {name}, tribe_name: {tribe_name}, "
                             f"tribe_value: {tribe_value}, language: {locale}")

                if tribe_value is not None:
                    if not await db_user.user_exists(tg_id=tg_id):
                        if tg_id in Config.SUPERUSER_IDS:
                            if locale in [language.Language.RU, language.Language.EN]:
                                await db_user.add_admin(tg_id, name, tribe_value, locale)
                            else:
                                await db_user.add_admin(tg_id, name, tribe_value)
                        else:
                            if locale in [language.Language.RU, language.Language.EN]:
                                await db_user.add_user(tg_id, name, tribe_value, locale)
                            else:
                                await db_user.add_user(tg_id, name, tribe_value)
                    else:
                        logger.warning(f"User already exists - tg_id: {tg_id}")
                else:
                    logger.warning(f"Tribe not found for tribe_name: {tribe_name}")

    except FileNotFoundError:
        logger.critical(f"File not found: {file_path}")
        raise
    except Exception as e:
        logger.critical(f"Error loading users from file: {e}")
        raise
