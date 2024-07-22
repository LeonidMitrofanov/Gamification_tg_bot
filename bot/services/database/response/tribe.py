import aiosqlite as sql
import logging
from typing import Optional

from bot.services.database.models.user import DBUser
from . import db_parameters as db_cfg
from .wallet import _generate_wallet_token, _add_wallet
from bot.enums.enums import UserRole

logger = logging.getLogger(__name__)


async def add_tribe(tribe_name: str, wallet_token: Optional[int] = None, tribe_id: Optional[int] = None) -> None:
    logger.debug(f"add_tribe called with tribe_name: {tribe_name}, wallet_token: {wallet_token}, tribe_id: {tribe_id}")

    # Generate wallet_token if not provided
    if wallet_token is None:
        wallet_token = _generate_wallet_token(tribe_name)

    try:
        async with sql.connect(db_cfg.path) as conn:
            logger.debug(f"Connected to the database: {db_cfg.path}")
            async with conn.cursor() as cursor:
                # Check if tribe already exists
                await cursor.execute('''
                    SELECT COUNT(*) FROM tribes WHERE tribe_name = ? OR tribe_id = ?
                ''', (tribe_name, tribe_id))
                count = (await cursor.fetchone())[0]

                if count > 0:
                    logger.warning(f"Tribe with name '{tribe_name}' or ID '{tribe_id}' already exists.")
                    return  # Exit the function if the tribe already exists

                if tribe_id is None:
                    # Insert a new tribe with auto-generated tribe_id
                    await cursor.execute('''
                        INSERT INTO tribes (tribe_name, wallet_token) VALUES (?, ?)
                    ''', (tribe_name, wallet_token))
                    logger.debug("Executed SQL insert statement")
                else:
                    # Insert a tribe with a specified tribe_id
                    await cursor.execute('''
                        INSERT INTO tribes (tribe_id, tribe_name, wallet_token) VALUES (?, ?, ?)
                    ''', (tribe_id, tribe_name, wallet_token))
                    logger.debug("Executed SQL insert statement with specified tribe_id")

            await conn.commit()
            logger.debug("Transaction committed")
        logger.info(
            f"Tribe '{tribe_name}' added successfully with wallet_token: {wallet_token} and tribe_id: {tribe_id}")
    except sql.Error as e:
        logger.critical(f"Error adding tribe: {e}")
        raise
