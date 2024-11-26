import psycopg2


class AnalyticsRepository:
    def __init__(self, database_url: str):
        print(f"Initializing AnalyticsRepository with URL: {database_url}", flush=True)
        self.database_url = database_url
        self._initialize_db()

    def _initialize_db(self):
        print(f"Connecting to database with URL: {self.database_url}", flush=True)
        conn = psycopg2.connect(self.database_url)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id SERIAL PRIMARY KEY,
            calendar_id INTEGER,
            action TEXT NOT NULL,
            details TEXT NOT NULL,
            owner TEXT NOT NULL,
            name TEXT NOT NULL
        )
        """)
        conn.commit()
        conn.close()

    def save_notification(self, notification: dict):
        conn = psycopg2.connect(self.database_url)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO notifications (calendar_id, action, details, owner, name)
        VALUES (%s, %s, %s, %s, %s)
        """, (
            notification["calendar_id"],
            notification["action"],
            notification["details"],
            notification["owner"],
            notification["name"]
        ))
        conn.commit()
        conn.close()

    def get_notifications(self):
        conn = psycopg2.connect(self.database_url)
        cursor = conn.cursor()
        cursor.execute("SELECT id, calendar_id, action, details, owner, name FROM notifications")
        notifications = cursor.fetchall()
        conn.close()
        return [
            {"id": row[0], "calendar_id": row[1], "action": row[2], "details": row[3], "owner": row[4], "name": row[5]}
            for row in notifications
        ]
