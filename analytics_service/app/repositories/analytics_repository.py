import sqlite3
import os

class AnalyticsRepository:
    def __init__(self):
        self.db_path = "/data/analytics.db"
        self._initialize_db()

    def _initialize_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            calendar_id INTEGER,
            action TEXT NOT NULL,
            details TEXT NOT NULL
        )
        """)
        conn.commit()
        conn.close()

    def process_notification(self, notification: dict):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO notifications (calendar_id, action, details)
        VALUES (?, ?, ?)do
        """, (notification["calendar_id"], notification["action"], notification["details"]))
        conn.commit()
        conn.close()

    def get_notifications(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM notifications")
        logs = cursor.fetchall()
        conn.close()

        return [{"id": row[0], "calendar_id": row[1], "action": row[2], "details": row[3]} for row in logs]

    def clear_notifications(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM notifications")
        conn.commit()
        conn.close()
