import aiosqlite as sql
import logging
from typing import Optional
from random import choice

from .. import db_config
from .wallet import _generate_wallet_token, _add_wallet
from bot.enums.enums import Tribe
from bot.services.database.models.tribe import Tribe as Tribe_model
from bot.exceptions.tribe import *

logger = logging.getLogger(__name__)


def _generate_tribe_id() -> int:
    logger.debug(f"Generate tribe_id")
    random_tribe = choice(list(Tribe))
    logger.debug(f"{random_tribe} chosen")
    return random_tribe.value


async def add_tribe(tribe_name: str, wallet_token: Optional[int] = None, tribe_id: Optional[int] = None) -> None:
    logger.debug(f"add_tribe called with tribe_name: {tribe_name}, wallet_token: {wallet_token}, tribe_id: {tribe_id}")

    # Generate wallet_token if not provided
    if wallet_token is None:
        wallet_token = _generate_wallet_token(tribe_name)

    try:
        async with sql.connect(db_config.path) as conn:
            logger.debug(f"Connected to the database: {db_config.path}")
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
        await _add_wallet(wallet_token)
        logger.info(
            f"Tribe '{tribe_name}' added successfully with wallet_token: {wallet_token} and tribe_id: {tribe_id}")
    except sql.Error as e:
        logger.critical(f"Error adding tribe: {e}")
        raise


async def get_tribe(tribe_id: int) -> Tribe_model:
    """
    Retrieve a tribe from the database by its ID.

    :param tribe_id: The ID of the tribe to retrieve.
    :return: A Tribe_model object if found.
    :raises TribeNotFoundError: If no tribe with the specified ID is found.
    """
    logger.debug(f"get_tribe called with ID {tribe_id}")

    query = "SELECT tribe_id, tribe_name, wallet_token FROM tribes WHERE tribe_id = ?"

    try:
        async with sql.connect(db_config.path) as conn:
            async with conn.execute(query, (tribe_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    tribe = Tribe_model(tribe_id=row[0], tribe_name=row[1], wallet_token=row[2])
                    logger.debug(f"Tribe found: {tribe}")
                    return tribe
                else:
                    logger.debug(f"No tribe found with ID {tribe_id}")
                    raise TribeNotFoundError(tribe_id)
    except sql.Error as e:
        logger.error(f"Error fetching tribe with ID {tribe_id}: {e}")
        raise
