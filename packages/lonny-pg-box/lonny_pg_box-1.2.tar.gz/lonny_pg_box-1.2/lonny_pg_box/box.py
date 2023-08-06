from .cfg import Configuration
from datetime import datetime, timedelta
from .logger import logger
from json import dumps

class Box:
    def __init__(self, db, name = Configuration.default_name):
        self._db = db
        self._name = name

    def _get(self, key, ** kwargs):
        logger.debug(f"Box: {self._name} fetching value for: {key}.")
        row = self._db.fetch_one(lambda o: f"""
            SELECT value FROM {Configuration.table}
            WHERE name = {o(self._name)}
            AND key = {o(key)}
        """)
        if row is None:
            if "default" not in kwargs:
                raise KeyError(self._name)
            return kwargs["default"]
        return row["value"]
        
    def get(self, key, default = None):
        return self._get(key, default = default)

    def __getitem__(self, key):
        return self._get(key)

    def __setitem__(self, key, value):
        logger.debug(f"Box: {self._name} setting value for: {key}.")
        self._db.execute(lambda o: f"""
            INSERT INTO {Configuration.table} VALUES (
                {o(self._name)}, 
                {o(key)}, 
                {o(dumps(value))}, 
                {o(datetime.utcnow())}
            ) ON CONFLICT (name, key) DO UPDATE SET
                value = {o(dumps(value))},
                update_dt = {o(datetime.utcnow())}
        """)

    @staticmethod
    def setup(db):
        logger.info("Creating box table.")
        db.execute(lambda o: f"""
            CREATE TABLE IF NOT EXISTS {Configuration.table} (
                name TEXT NOT NULL,
                key TEXT NOT NULL,
                value JSONB NOT NULL,
                update_dt TIMESTAMP NOT NULL,
                PRIMARY KEY(name, key)
            );
        """)

    @staticmethod
    def destroy_old_values(db, *, max_age = timedelta(Configuration.stale_value_days)):
        logger.info("Destroying old box values.")
        db.execute(lambda o: f"""
            DELETE FROM {Configuration.table}
            WHERE update_dt < {o(datetime.utcnow() - max_age)}
        """)