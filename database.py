"""
database.py — SQLite storage for sensor readings
"""
import sqlite3
import json
import time

class Database:
    def __init__(self, path: str = "sensors.db"):
        self.path = path

    def init(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS readings (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp   REAL,
                    temperature REAL,
                    humidity    REAL,
                    light       REAL,
                    motion      INTEGER,
                    air_quality REAL,
                    sound       REAL,
                    raw_json    TEXT
                )
            """)
            conn.commit()

    def insert(self, data: dict):
        with sqlite3.connect(self.path) as conn:
            conn.execute("""
                INSERT INTO readings
                    (timestamp, temperature, humidity, light, motion, air_quality, sound, raw_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get("server_time", time.time()),
                data.get("temperature"),
                data.get("humidity"),
                data.get("light"),
                1 if data.get("motion") else 0,
                data.get("air_quality"),
                data.get("sound"),
                json.dumps(data),
            ))
            conn.commit()

    def get_recent(self, limit: int = 50) -> list:
        with sqlite3.connect(self.path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM readings ORDER BY timestamp DESC LIMIT ?", (limit,)
            ).fetchall()
        return [dict(r) for r in rows]

    def get_latest(self) -> dict:
        with sqlite3.connect(self.path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM readings ORDER BY timestamp DESC LIMIT 1"
            ).fetchone()
        return dict(row) if row else {}
