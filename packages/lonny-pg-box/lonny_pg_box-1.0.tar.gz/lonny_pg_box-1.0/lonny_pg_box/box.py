from .cfg import Configuration
from .logger import logger
from json import dumps

class Box:
    def __init__(self, db):
        self._db = db

    def __getitem__(self, key):
        logger.debug(f"Fetching value for: {key}.")
        row = self._db.fetch_one(lambda o: f"""
            SELECT value FROM {Configuration.table}
            WHERE key = {o(key)}
        """)
        return None if row is None else row["value"]

    def __setitem__(self, key, value):
        logger.debug(f"Setting value for: {key}.")
        self._db.execute(lambda o: f"""
            INSERT INTO {Configuration.table} VALUES (
                {o(key)}, {o(dumps(value))}
            ) ON CONFLICT (key) DO UPDATE SET
                value = {o(dumps(value))}
        """)

    @staticmethod
    def setup(db):
        logger.debug("Creating box table.")
        db.execute(lambda o: f"""
            CREATE TABLE IF NOT EXISTS {Configuration.table} (
                key TEXT NOT NULL,
                value JSONB NOT NULL,
                PRIMARY KEY(key)
            );
        """)