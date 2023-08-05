from .cfg import Configuration
from .logger import logger
from json import dumps

class Box:
    def __init__(self, db, name):
        self._db = db
        self._name = name

    def get(self, ** kwargs):
        logger.debug(f"Fetching value for: {self._name}.")
        row = self._db.fetch_one(lambda o: f"""
            SELECT value FROM {Configuration.table}
            WHERE key = {o(self._name)}
        """)
        if row is None:
            if "default" not in kwargs:
                raise KeyError(self._name)
            return kwargs["default"]
        return row["value"]

    def set(self, value):
        logger.debug(f"Setting value for: {self._name}.")
        self._db.execute(lambda o: f"""
            INSERT INTO {Configuration.table} VALUES (
                {o(self._name)}, {o(dumps(value))}
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