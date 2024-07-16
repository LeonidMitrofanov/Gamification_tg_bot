import sqlite3
import logging
from src.config import Config
from contextlib import closing

logger = logging.getLogger(__name__)


class DataBase:
    def __init__(self):
        """Initialize the data with required tables."""
        try:
            with sqlite3.connect(Config.DB_PATH) as conn:
                with closing(conn.cursor()) as cursor:
                    # Enable foreign key support
                    cursor.execute('PRAGMA foreign_keys = ON;')

                    # Create users table
                    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tg_id INTEGER UNIQUE,
                        tg_tag TEXT,
                        name TEXT,
                        klan_id INTEGER,
                        description TEXT,
                        photo_path TEXT,
                        FOREIGN KEY(klan_id) REFERENCES klan(id)
                    )
                    ''')

                    # Create klan table
                    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS klan (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        whalet_id INTEGER,
                        FOREIGN KEY(whalet_id) REFERENCES whalets(id)
                    )
                    ''')

                    # Create event_state table
                    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS event_state (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        state TEXT
                    )
                    ''')

                    # Create event table
                    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS event (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        description TEXT,
                        dataTime TEXT,
                        owner_id INTEGER,
                        approver_id INTEGER,
                        state INTEGER,
                        FOREIGN KEY(owner_id) REFERENCES users(id),
                        FOREIGN KEY(approver_id) REFERENCES users(id),
                        FOREIGN KEY(state) REFERENCES event_state(id)
                    )
                    ''')

                    # Create event_subscribes table
                    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS event_subscribes (
                        event_id INTEGER,
                        user_id INTEGER,
                        FOREIGN KEY(event_id) REFERENCES event(id),
                        FOREIGN KEY(user_id) REFERENCES users(id)
                    )
                    ''')

                    # Create whalets table
                    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS whalets (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        volume REAL
                    )
                    ''')

                    conn.commit()

                    # Insert initial states into event_state table
                    cursor.executemany('''
                    INSERT OR IGNORE INTO event_state (id, state) VALUES (?, ?)
                    ''', [
                        (0, 'pending'),
                        (1, 'approved'),
                        (2, 'rejected'),
                        (3, 'completed'),
                        (4, 'in progress')
                    ])

                    # Insert initial clans into klan table
                    cursor.executemany('''
                    INSERT OR IGNORE INTO klan (id, name, whalet_id) VALUES (?, ?, ?)
                    ''', [
                        (1, 'Aqua', None),
                        (2, 'Ignis', None),
                        (3, 'Air', None),
                        (4, 'Terra', None)
                    ])
                    conn.commit()

            logger.info("Database initialized successfully")
        except sqlite3.Error as e:
            logger.exception(f"Error initializing data: {e}")

    async def add_users(self, user_id, username, first_name, last_name):
        pass

    async def get_user(self, user_id):
        pass
