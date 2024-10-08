import aiosqlite as sql
import logging
from typing import Optional

from bot.services.database.models.user import DBUser
from bot.services.database import db_config
from .wallet import _generate_wallet_token, _add_wallet
from .tribe import _generate_tribe_id
from bot.enums.enums import UserRole
from bot.enums.language import Language

logger = logging.getLogger(__name__)


async def _add_user(tg_id: int, name: str, user_role: int,
                    tribe_id: Optional[int] = None, language: str = Language.DEFAULT) -> None:
    logger.debug(f"add_user called with tg_id: {tg_id}, name: {name}, tribe_id: {tribe_id},"
                 f" language: {language}, user_role: {user_role}")

    if tribe_id is None:
        tribe_id = _generate_tribe_id()

    wallet_token = _generate_wallet_token(tg_id)

    try:
        async with sql.connect(db_config.path) as conn:
            logger.debug(f"Connected to the database: {db_config.path}")
            async with conn.cursor() as cursor:
                await cursor.execute('''
                INSERT INTO users (tg_id, name, tribe_id, wallet_token, language, role_id) VALUES (?, ?, ?, ?, ?, ?)
                ''', (tg_id, name, tribe_id, wallet_token, language, user_role))
            await conn.commit()
            logger.debug("Transaction committed")
        await _add_wallet(wallet_token)
        logger.info(f"User \"{name} tg_id: {tg_id}\" added successfully")
    except sql.Error as e:
        logger.error(f"Error adding user: {e}")
        raise


async def add_user(tg_id: int, name: str, tribe_id: Optional[int] = None,
                   language: Optional[str] = Language.DEFAULT) -> None:
    if (language is None) or not (language in Language.ALL):
        language = Language.DEFAULT
    await _add_user(tg_id, name, UserRole.USER.value, tribe_id, language)


async def add_admin(tg_id: int, name: str, tribe_id: Optional[int] = None,
                    language: Optional[str] = Language.DEFAULT) -> None:
    if (language is None) or not (language in Language.ALL):
        language = Language.DEFAULT
    await _add_user(tg_id, name, UserRole.ADMIN.value, tribe_id, language)


async def user_exists(user_id: Optional[int] = None, tg_id: Optional[int] = None) -> bool:
    logger.debug(f"user_exists called with user_id: {user_id}, tg_id: {tg_id}")

    if user_id is None and tg_id is None:
        logger.error("Either user_id or tg_id must be provided.")
        return False

    try:
        async with sql.connect(db_config.path) as conn:
            logger.debug(f"Connected to the database: {db_config.path}")
            async with conn.cursor() as cursor:
                if user_id is not None:
                    await cursor.execute('SELECT COUNT(*) FROM users WHERE user_id = ?', (user_id,))
                else:
                    await cursor.execute('SELECT COUNT(*) FROM users WHERE tg_id = ?', (tg_id,))
                logger.debug("Executed SQL select statement")

                count = (await cursor.fetchone())[0]
                logger.debug(f"User count: {count}")
                return count > 0
    except sql.Error as e:
        logger.exception(f"Error checking if user exists: {e}")
        return False


async def get_user_count() -> int:
    logger.debug("get_user_count called")

    try:
        async with sql.connect(db_config.path) as conn:
            logger.debug(f"Connected to the database: {db_config.path}")
            async with conn.cursor() as cursor:
                await cursor.execute('SELECT COUNT(*) FROM users')
                logger.debug("Executed SQL select statement")

                count = await cursor.fetchone()[0]
                logger.debug(f"User count: {count}")
                return count
    except sql.Error as e:
        logger.exception(f"Error getting user count: {e}")
        return 0


async def get_user(tg_id: Optional[int] = None, user_id: Optional[int] = None) -> Optional[DBUser]:
    logger.debug(f"get_user called with tg_id: {tg_id}, user_id: {user_id}")

    if tg_id is None and user_id is None:
        logger.error("At least one of tg_id or user_id must be provided.")
        return None

    try:
        async with sql.connect(db_config.path) as conn:
            logger.debug(f"Connected to the database: {db_config.path}")
            async with conn.cursor() as cursor:
                if user_id is not None:
                    await cursor.execute('''
                        SELECT user_id, tg_id, tg_teg, name, tribe_id, role_id,
                        wallet_token, language, description, photo_path
                        FROM users
                        WHERE user_id = ?
                    ''', (user_id,))
                elif tg_id is not None:
                    await cursor.execute('''
                        SELECT user_id, tg_id, tg_teg, name, tribe_id, role_id, 
                        wallet_token, language, description, photo_path
                        FROM users
                        WHERE tg_id = ?
                    ''', (tg_id,))

                logger.debug("Executed SQL select statement")

                row = await cursor.fetchone()
                if row:
                    logger.debug(f"User found: {row}")
                    user = DBUser(*row)
                    logger.debug("Successfully retrieved user")
                    return user
                else:
                    logger.debug(
                        f"No user found with {'tg_id' if tg_id is not None else 'user_id'}: "
                        f"{tg_id if tg_id is not None else user_id}")
                    return None
    except sql.Error as e:
        logger.exception(f"Error retrieving user info: {e}")
        return None


async def update_user_tg_teg(tg_id: int, tg_teg: str) -> bool:
    logger.debug(f"Updating tg_teg for user with tg_id: {tg_id} to {tg_teg}")
    try:
        async with sql.connect(db_config.path) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute('''
                    UPDATE users SET tg_teg = ? WHERE tg_id = ?
                ''', (tg_teg, tg_id))
            await conn.commit()
        logger.info(f"tg_teg updated for user with tg_id: {tg_id}, tg_teg: {tg_teg}")
        return True
    except sql.Error as e:
        logger.critical(f"Error updating tg_teg: {e}")
        return False
