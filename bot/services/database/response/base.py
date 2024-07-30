import aiosqlite as sql
import logging

from bot.enums.enums import EventState, UserRole, Tribe
from bot.services.database import db_config
from .tribe import add_tribe

logger = logging.getLogger(__name__)


async def initialize(db_path: str):
    db_config.path = db_path
    logger.debug(f"Initializing database with path: {db_config.path}")

    try:
        async with sql.connect(db_config.path) as conn:
            async with conn.cursor() as cursor:
                # Enable foreign key support
                await cursor.execute('PRAGMA foreign_keys = ON;')
                logger.debug("Enabled foreign key support")

                await _create_tables(conn)
                logger.debug("Tables creation process completed")

                await _insert_initial_data(conn)
                logger.debug("Initial data insertion process completed")

            await conn.commit()
            logger.debug("Transaction committed")

        logger.info("Database initialized successfully")
    except sql.Error as e:
        logger.critical(f"Error initializing database: {e}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error during database initialization: {e}")
        raise


async def _create_tables(conn):
    logger.debug("Starting to create tables")
    try:
        async with conn.cursor() as cursor:
            await _create_users_table(cursor)
            await _create_tribes_table(cursor)
            await _create_event_table(cursor)
            await _create_event_states_table(cursor)
            await _create_event_subscribers_table(cursor)
            await _create_wallets_table(cursor)
            await _create_user_roles_table(cursor)
            await _create_achievements_table(cursor)
            await _create_user_achievements_table(cursor)
        logger.info("All tables created successfully")
    except sql.Error as e:
        logger.critical(f"Critical error creating tables: {e}")
        raise


async def _insert_initial_data(conn):
    logger.debug("Inserting initial data")
    try:
        async with conn.cursor() as cursor:
            await _initial_tribes()
            await _initial_eventState(cursor)
            await _initial_userRoles(cursor)
        logger.info("Initial data inserted successfully")
    except Exception as e:
        logger.critical(f"Critical error inserting initial data: {e}")
        raise


async def _create_users_table(cursor):
    logger.debug("Creating users table")
    try:
        await cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER UNIQUE NOT NULL,
            tg_teg TEXT UNIQUE,
            name TEXT NOT NULL,
            tribe_id INTEGER NOT NULL,
            role_id INTEGER NOT NULL,
            wallet_token INTEGER UNIQUE NOT NULL,
            language TEXT NOT NULL,
            description TEXT,
            photo_path TEXT,
            FOREIGN KEY(tribe_id) REFERENCES tribes(tribe_id),
            FOREIGN KEY(wallet_token) REFERENCES wallets(wallet_token),
            FOREIGN KEY(role_id) REFERENCES userRoles(userRole_id)
        )
        ''')
        logger.info("Users table created successfully")
    except sql.Error as e:
        logger.critical(f"Critical error creating users table: {e}")
        raise


async def _create_tribes_table(cursor):
    logger.debug("Creating tribes table")
    try:
        await cursor.execute('''
        CREATE TABLE IF NOT EXISTS tribes (
            tribe_id INTEGER PRIMARY KEY AUTOINCREMENT,
            tribe_name TEXT NOT NULL,
            wallet_token INTEGER NOT NULL,
            FOREIGN KEY(wallet_token) REFERENCES wallets(wallet_token)
        )
        ''')
        logger.info("Tribes table created successfully")
    except sql.Error as e:
        logger.critical(f"Critical error creating tribes table: {e}")
        raise


async def _create_event_table(cursor):
    logger.debug("Creating event table")
    try:
        await cursor.execute('''
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
            FOREIGN KEY(state) REFERENCES eventStates(eventState_id)
        )
        ''')
        logger.info("Event table created successfully")
    except sql.Error as e:
        logger.critical(f"Critical error creating event table: {e}")
        raise


async def _create_event_states_table(cursor):
    logger.debug("Creating eventStates table")
    try:
        await cursor.execute('''
        CREATE TABLE IF NOT EXISTS eventStates (
            eventState_id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT NOT NULL
        )
        ''')
        logger.info("EventStates table created successfully")
    except sql.Error as e:
        logger.critical(f"Critical error creating eventStates table: {e}")
        raise


async def _create_event_subscribers_table(cursor):
    logger.debug("Creating event_subscribers table")
    try:
        await cursor.execute('''
        CREATE TABLE IF NOT EXISTS event_subscribers (
            event_id INTEGER NOT NULL,
            subscriber_id INTEGER NOT NULL,
            FOREIGN KEY(event_id) REFERENCES event(event_id),
            FOREIGN KEY(subscriber_id) REFERENCES users(user_id)
        )
        ''')
        logger.info("Event_subscribers table created successfully")
    except sql.Error as e:
        logger.critical(f"Critical error creating event_subscribers table: {e}")
        raise


async def _create_wallets_table(cursor):
    logger.debug("Creating wallets table")
    try:
        await cursor.execute('''
        CREATE TABLE IF NOT EXISTS wallets (
            wallet_token INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            balance REAL DEFAULT 0
        )
        ''')
        logger.info("Wallets table created successfully")
    except sql.Error as e:
        logger.critical(f"Critical error creating wallets table: {e}")
        raise


async def _create_user_roles_table(cursor):
    logger.debug("Creating userRoles table")
    try:
        await cursor.execute('''
        CREATE TABLE IF NOT EXISTS userRoles (
            userRole_id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT NOT NULL
        )
        ''')
        logger.info("UserRoles table created successfully")
    except sql.Error as e:
        logger.critical(f"Critical error creating userRoles table: {e}")
        raise


async def _create_achievements_table(cursor):
    logger.debug("Creating achievements table")
    try:
        await cursor.execute('''
        CREATE TABLE IF NOT EXISTS achievements (
            achievement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            photo_path TEXT,
            bonus REAL DEFAULT 0
        )
        ''')
        logger.info("Achievements table created successfully")
    except sql.Error as e:
        logger.critical(f"Critical error creating achievements table: {e}")
        raise


async def _create_user_achievements_table(cursor):
    logger.debug("Creating user_achievements table")
    try:
        await cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_achievements (
            user_id INTEGER NOT NULL,
            achievement_id INTEGER NOT NULL,
            count INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(user_id),
            FOREIGN KEY(achievement_id) REFERENCES achievements(achievement_id)
        )
        ''')
        logger.info("User_achievements table created successfully")
    except sql.Error as e:
        logger.critical(f"Critical error creating user_achievements table: {e}")
        raise


async def _initial_tribes():
    logger.debug("Inserting initial tribes")
    try:
        await add_tribe('Aqua', Tribe.AQUA.value, Tribe.AQUA.value)
        await add_tribe('Ignis', Tribe.IGNIS.value, Tribe.IGNIS.value)
        # await add_tribe('Air', Tribe.AIR.value, Tribe.AIR.value)
        # await add_tribe('Terra', Tribe.TERRA.value, Tribe.TERRA.value)
        logger.info("Initial tribes inserted successfully")
    except Exception as e:
        logger.critical(f"Critical error inserting initial tribes: {e}")
        raise


async def _initial_eventState(cursor):
    logger.debug("Inserting initial event states")
    try:
        await cursor.executemany('''
            INSERT OR IGNORE INTO eventStates (eventState_id, state) VALUES (?, ?)
            ''', [
            (EventState.ON_REVIEW.value, 'on_review'),  # На рассмотрении
            (EventState.APPROVED.value, 'approved'),  # Одобрено
            (EventState.REJECTED.value, 'rejected'),  # Отклонено
            (EventState.IN_PROGRESS.value, 'in_progress'),  # В процессе
            (EventState.COMPLETED.value, 'completed')  # Завершено
        ])
        logger.info("Initial event states inserted successfully")
    except sql.Error as e:
        logger.critical(f"Critical error inserting initial event states: {e}")
        raise


async def _initial_userRoles(cursor):
    logger.debug("Inserting initial user roles")
    try:
        await cursor.executemany('''
            INSERT OR IGNORE INTO userRoles (userRole_id, role_name) VALUES (?, ?)
            ''', [
            (UserRole.USER.value, 'user'),
            (UserRole.ADMIN.value, 'admin'),
        ])
        logger.info("Initial user roles inserted successfully")
    except sql.Error as e:
        logger.critical(f"Critical error inserting initial user roles: {e}")
        raise
