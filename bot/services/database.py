import sqlite3 as sql
import logging
from contextlib import closing
from typing import Optional

from .models import *

logger = logging.getLogger(__name__)

_db_path: Optional[str] = None


def initialize(db_path: str):
    global _db_path
    _db_path = db_path
    try:
        with sql.connect(_db_path) as conn:
            with closing(conn.cursor()) as cursor:
                # Enable foreign key support
                cursor.execute('PRAGMA foreign_keys = ON;')

                _create_tables(cursor)
                _insert_initial_data(cursor)

            conn.commit()

        logger.info("Database initialized successfully")
    except sql.Error as e:
        logger.critical(f"Error initializing data: {e}")
        exit()


def _create_tables(cursor):
    # users
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER UNIQUE NOT NULL,
        tg_teg TEXT UNIQUE,
        name TEXT NOT NULL,
        tribe_id INTEGER NOT NULL,
        role_id INTEGER NOT NULL,
        wallet_token INTEGER UNIQUE NOT NULL,
        description TEXT,
        photo_path TEXT,
        FOREIGN KEY(tribe_id) REFERENCES tribes(tribe_id)
        FOREIGN KEY(wallet_token) REFERENCES wallets(wallet_token)
        FOREIGN KEY(role_id) REFERENCES userRoles(role_id)
    )
    ''')

    # tribes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tribes (
        tribe_id INTEGER PRIMARY KEY AUTOINCREMENT,
        tribe_name TEXT NOT NULL,
        wallet_token INTEGER NOT NULL,
        FOREIGN KEY(wallet_token) REFERENCES wallets(wallet_token)
    )
    ''')

    # event
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS event (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        dataTime TEXT NOT NULL,
        owner_id INTEGER NOT NULL,
        approver_id INTEGER NOT NULL,
        state INTEGER NOT NULL,
        FOREIGN KEY(owner_id) REFERENCES users(user_id),
        FOREIGN KEY(approver_id) REFERENCES users(user_id),
        FOREIGN KEY(state) REFERENCES eventState(eventState_id)
    )
    ''')

    # eventStates
    cursor.execute('''
       CREATE TABLE IF NOT EXISTS eventStates (
           eventState_id INTEGER PRIMARY KEY AUTOINCREMENT,
           state TEXT NOT NULL
       )
       ''')

    # event_subscribers
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS event_subscribers (
        event_id INTEGER NOT NULL,
        subscriber_id INTEGER NOT NULL,
        FOREIGN KEY(event_id) REFERENCES event(event_id),
        FOREIGN KEY(subscriber_id) REFERENCES users(user_id)
    )
    ''')

    # wallets
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS wallets (
        wallet_token INTEGER PRIMARY KEY AUTOINCREMENT,
        balance REAL DEFAULT 0
    )
    ''')

    # userRoles
    cursor.execute('''
   CREATE TABLE IF NOT EXISTS userRoles (
       userRole_id INTEGER PRIMARY KEY AUTOINCREMENT,
       role_name TEXT NOT NULL
   )
   ''')


def _insert_initial_data(cursor):
    # tribes
    cursor.executemany('''
    INSERT OR IGNORE INTO tribes (tribe_id, tribe_name, wallet_token) VALUES (?, ?, ?)
    ''', [
        (Tribe.AQUA.value, 'Aqua', None),
        (Tribe.IGNIS.value, 'Ignis', None),
        (Tribe.AIR.value, 'Air', None),
        (Tribe.TERRA.value, 'Terra', None)
    ])

    # eventState
    cursor.executemany('''
        INSERT OR IGNORE INTO eventStates (eventState_id, state) VALUES (?, ?)
        ''', [
        (EventState.ON_REVIEW.value, 'on_review'),      # На рассмотрении
        (EventState.APPROVED.value, 'approved'),        # Одобрено
        (EventState.REJECTED.value, 'rejected'),        # Отклонено
        (EventState.IN_PROGRESS.value, 'in_progress'),  # В процессе
        (EventState.COMPLETED.value, 'completed')       # Завершено
    ])

    # userRoles
    cursor.executemany('''
        INSERT OR IGNORE INTO userRoles (userRole_id, role_name) VALUES (?, ?)
        ''', [
        (UserRole.USER.value, 'user'),
        (UserRole.ADMIN.value, 'admin'),
    ])


def get_user_count() -> int:
    logger.debug("get_user_count called")

    if _db_path is None:
        logger.error("Database path is not set. Please initialize the database first.")
        return 0

    try:
        with sql.connect(_db_path) as conn:
            logger.debug(f"Connected to the database: {_db_path}")
            with closing(conn.cursor()) as cursor:
                cursor.execute('SELECT COUNT(*) FROM users')
                logger.debug("Executed SQL select statement")

                count = cursor.fetchone()[0]
                logger.debug(f"User count: {count}")
                return count
    except sql.Error as e:
        logger.exception(f"Error getting user count: {e}")
        return 0


def user_exists(user_id: Optional[int] = None, tg_id: Optional[int] = None) -> bool:
    logger.debug(f"user_exists called with user_id: {user_id}, tg_id: {tg_id}")

    if user_id is None and tg_id is None:
        logger.error("Either user_id or tg_id must be provided.")
        return False

    try:
        with sql.connect(_db_path) as conn:
            logger.debug(f"Connected to the database: {_db_path}")
            with closing(conn.cursor()) as cursor:
                if user_id is not None:
                    cursor.execute('SELECT COUNT(*) FROM users WHERE user_id = ?', (user_id,))
                else:
                    cursor.execute('SELECT COUNT(*) FROM users WHERE tg_id = ?', (tg_id,))
                logger.debug("Executed SQL select statement")

                count = cursor.fetchone()[0]
                logger.debug(f"User count: {count}")
                return count > 0
    except sql.Error as e:
        logger.exception(f"Error checking if user exists: {e}")
        return False


def _generate_wallet_token(target: object) -> int:
    # TODO: Implementation
    return int(target)


async def _add_wallet(token: int, balance: float = 0) -> None:
    logger.debug(f"add_wallet called with token: {token}, balance: {balance}")
    try:
        with sql.connect(_db_path) as conn:
            logger.debug(f"Connected to the database: {_db_path}")
            with closing(conn.cursor()) as cursor:
                cursor.execute('''
                INSERT INTO wallets (wallet_token, balance) VALUES (?, ?)
                ''', (token, balance))
                logger.debug("Executed SQL insert statement")
            conn.commit()
            logger.debug("Transaction committed")
        logger.info(f"Wallet with token: {token} added successfully with balance: {balance}")
    except sql.Error as e:
        logger.exception(f"Error adding wallet: {e}")


async def _add_user(tg_id: int, name: str, tribe_id: int, user_role: int) -> None:
    logger.debug(
        f"add_user called with tg_id: {tg_id}, name: {name}, tribe_id: {tribe_id}, "
        f" user_role: {user_role}")

    wallet_token = _generate_wallet_token(tg_id)
    await _add_wallet(wallet_token)

    try:
        with sql.connect(_db_path) as conn:
            logger.debug(f"Connected to the database: {_db_path}")
            with closing(conn.cursor()) as cursor:
                cursor.execute('''
                INSERT INTO users (tg_id, name, tribe_id, wallet_token, role_id) VALUES (?, ?, ?, ?, ?)
                ''', (tg_id, name, tribe_id, wallet_token, user_role))
                logger.debug("Executed SQL insert statement")
            conn.commit()
            logger.debug("Transaction committed")
        logger.info(f"User \"{name} tg_id: {tg_id}\" added successfully")
    except sql.Error as e:
        logger.exception(f"Error adding user: {e}")


async def add_user(tg_id: int, name: str, tribe_id: int) -> None:
    await _add_user(tg_id, name, tribe_id, UserRole.USER.value)


async def add_admin(tg_id: int, name: str, tribe_id: int) -> None:
    await _add_user(tg_id, name, tribe_id, UserRole.ADMIN.value)
