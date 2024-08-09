import aiosqlite as sql
import logging

from .. import db_config

logger = logging.getLogger(__name__)


async def get_balance(wallet_token: int) -> float:
    """
    Get the balance of a wallet by its token.

    :param wallet_token: The token of the wallet.
    :return: The balance of the wallet.
    :raises ValueError: If the wallet token is not found.
    """
    logger.debug(f"Fetching balance for wallet token: {wallet_token}")

    async with sql.connect(db_config.path) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('SELECT balance FROM wallets WHERE wallet_token = ?', (wallet_token,))
            result = await cursor.fetchone()

            if result is None:
                logger.error(f"Wallet token {wallet_token} not found.")
                raise ValueError(f"Wallet token {wallet_token} not found.")

            balance = result[0]
            logger.debug(f"Balance for wallet token {wallet_token}: {balance}")
            return balance


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
        logger.critical(f"Error adding wallet: {e}")
        raise
