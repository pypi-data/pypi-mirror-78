from secrets import token_hex
from time import sleep
from contextlib import contextmanager
from datetime import datetime, timedelta
from .cfg import Configuration
from .logger import logger

class Lock:
    def __init__(self, db, name = Configuration.default_lock_name):
        self._db = db
        self._name = name

    @contextmanager
    def guard(self, slug, *, duration = timedelta(minutes = Configuration.stale_guard_minutes)):
        try:
            now_dt = datetime.utcnow()
            row = self._db.fetch_one(lambda o: f"""
                INSERT INTO {Configuration.table} VALUES (
                    {o(self._name)},
                    {o(slug)},
                    {o(now_dt)}
                ) ON CONFLICT (name, slug) DO UPDATE
                    SET lock_dt = {o(now_dt)}
                    WHERE {Configuration.table}.lock_dt IS NULL 
                    OR {Configuration.table}.lock_dt < {o(now_dt - duration)} 
                RETURNING *           
            """)
            yield row is not None
        finally:
            self._db.execute(lambda o: f"""
                DELETE FROM {Configuration.table}
                WHERE name = {o(self._name)} 
                AND slug = {o(slug)}
            """  )

    @staticmethod
    def setup(db):
        logger.info("Creating lock table.")
        db.execute(lambda o: f"""
            CREATE TABLE IF NOT EXISTS {Configuration.table} (
                name TEXT NOT NULL,
                slug TEXT NOT NULL,
                lock_dt TIMESTAMP NULL,
                PRIMARY KEY(name, slug)
            );
        """)

    @staticmethod
    def destroy_old_guards(db, *, max_age = timedelta(days = Configuration.old_guard_days)):
        min_lock_dt = datetime.utcnow() - max_age
        db.execute(lambda o: f"""
            DELETE FROM {Configuration.table}
            WHERE lock_dt < {o(min_lock_dt)}
        """)