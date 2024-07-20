import sqlite3 as sql
import logging
from contextlib import closing
from typing import Optional, Dict, Any

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
        logger.exception(f"Error initializing data: {e}")


def _create_tables(cursor):
    # users
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER UNIQUE NOT NULL,
        name TEXT NOT NULL,
        klan_id INTEGER NOT NULL,
        whalet_id INTEGER UNIQUE NOT NULL,
        description TEXT,
        photo_path TEXT,
        FOREIGN KEY(klan_id) REFERENCES klan(klan_id)
        FOREIGN KEY(whalet_id) REFERENCES whalets(whalet_id)
    )
    ''')  # TODO: Add role

    # klan
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS klan (
        klan_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        whalet_id INTEGER NOT NULL,
        FOREIGN KEY(whalet_id) REFERENCES whalets(whalet_id)
    )
    ''')

    # eventState
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS eventState (
        eventState_id INTEGER PRIMARY KEY AUTOINCREMENT,
        state TEXT NOT NULL
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

    # event_subscribes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS event_subscribes (
        event_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY(event_id) REFERENCES event(event_id),
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    ''')

    # whalets
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS whalets (
        whalet_id INTEGER PRIMARY KEY AUTOINCREMENT,
        volume REAL DEFAULT 0
    )
    ''')


def _insert_initial_data(cursor):
    cursor.executemany('''
    INSERT OR IGNORE INTO eventState (eventState_id, state) VALUES (?, ?)
    ''', [
        (0, 'on_review'),  # На рассмотрении
        (1, 'approved'),  # Одобрено
        (2, 'rejected'),  # Отклонено
        (3, 'in_progress'),  # В процессе
        (4, 'completed')  # Завершено
    ])

    cursor.executemany('''
    INSERT OR IGNORE INTO klan (klan_id, name, whalet_id) VALUES (?, ?, ?)
    ''', [
        (1, 'Aqua', None),
        (2, 'Ignis', None),
        (3, 'Air', None),
        (4, 'Terra', None)
    ])


async def add_user(tg_id: int, username: str, klan_id: int, whalet_id: int) -> None:
    try:
        with sql.connect(_db_path) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute('''
                INSERT INTO users (tg_id, name, klan_id, whalet_id) VALUES (?, ?, ?, ?)
                ''', (tg_id, username, klan_id, whalet_id))
            conn.commit()
        logger.info(f"User \"{username} | tg_id: {tg_id}\" added successfully")
    except sql.Error as e:
        logger.exception(f"Error adding user: {e}")


async def get_user(user_id: int) -> Optional[Dict[str, Any]]:
    try:
        with sql.connect(_db_path) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute('''
                SELECT * FROM users WHERE tg_id = ?
                ''', (user_id,))
                row = cursor.fetchone()
                if row:
                    return {
                        "id": row[0],
                        "tg_id": row[1],
                        "tg_tag": row[2],
                        "name": row[3],
                        "klan_id": row[4],
                        "description": row[5],
                        "photo_path": row[6]
                    }
                return None
    except sql.Error as e:
        logger.exception(f"Error retrieving user: {e}")
        return None
