import aiosqlite as sql
import logging

from .. import db_config

logger = logging.getLogger(__name__)


def _generate_wallet_token(target: object) -> int:
    logger.debug(f"Generate new wallet token by {target}")
    # TODO: Implementation
    return int(target)


async def _add_wallet(token: int, balance: float = 0) -> None:
    logger.debug(f"add_wallet called with token: {token}, balance: {balance}")
    try:
        async with sql.connect(db_config.path) as conn:
            logger.debug(f"Connected to the database: {db_config.path}")
            async with conn.cursor() as cursor:
                await cursor.execute('''
                INSERT INTO wallets (wallet_token, balance) VALUES (?, ?)
                ''', (token, balance))
                logger.debug("Executed SQL insert statement")
            await conn.commit()
            logger.debug("Transaction committed")
        logger.info(f"Wallet with token: {token} added successfully with balance: {balance}")
    except sql.Error as e:
        logger.exception(f"Error adding wallet: {e}")
