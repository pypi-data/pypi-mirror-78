from .logger import logger
from .cfg import Configuration
from datetime import datetime, timedelta
from contextlib import contextmanager
import json

class Queue():
    def __init__(self, db, name):
        self._db = db
        self._name = name

    def _consume(self, id):
        self._db.execute(lambda o: f"""
            DELETE FROM {Configuration.table}
            WHERE id = {o(id)}
        """)
        logger.debug(f"Message: {id} consumed")

    def _get(self):
        while True:
            now_dt = datetime.utcnow()
            cutoff_dt = now_dt - timedelta(seconds = Configuration.unlock_seconds)
            row = self._db.fetch_one(lambda o: f"""
                UPDATE {Configuration.table} 
                SET lock_dt = {o(now_dt)},
                attempts = attempts - 1
                WHERE id = (
                    SELECT id FROM {Configuration.table}
                    WHERE name = {o(self._name)}
                    AND (lock_dt IS NULL OR lock_dt < {o(cutoff_dt)})
                    FOR UPDATE SKIP LOCKED
                    LIMIT 1
                ) RETURNING *
            """)
            if row is None:
                return None, None
            if row["attempts"] < 0:
                self._consume(row["id"])
                continue
            return row["id"], row["payload"]

    def put(self, payload, *, attempts = 3):
        logger.info(f"Queue: {self._name} enqueued with message: {json.dumps(payload)}.")
        self._db.execute(lambda o: f"""
            INSERT INTO {Configuration.table} VALUES (
                DEFAULT,
                {o(self._name)},
                {o(json.dumps(payload))},
                NULL,
                {o(attempts)}
            );
        """)
    
    @contextmanager
    def get(self):
        id, payload = self._get()
        if id is not None:
            logger.info(f"Queue: {self._name} has dequeued message: {json.dumps(payload)}")
            yield payload
            self._consume(id)
        else:
            yield None

    @staticmethod
    def setup(db):
        db.execute(lambda o: f"""
            CREATE TABLE IF NOT EXISTS {Configuration.table} (
                id SERIAL,
                name TEXT NOT NULL,
                payload JSONB NOT NULL,
                lock_dt TIMESTAMP NULL,
                attempts INTEGER NOT NULL,
                PRIMARY KEY(id)
            );
        """)
        db.execute(lambda o: f"""
            CREATE INDEX IF NOT EXISTS {Configuration.table}_name_ix
                ON {Configuration.table}(name);
        """)