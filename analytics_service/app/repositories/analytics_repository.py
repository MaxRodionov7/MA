import psycopg2


class AnalyticsRepository:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self._initialize_db()

    def _initialize_db(self):
        conn = psycopg2.connect(self.database_url)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            action TEXT NOT NULL,
            calendar_id INTEGER,
            name TEXT,
            owner TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()
        conn.close()

    def get_all_events(self):
        conn = psycopg2.connect(self.database_url)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events")
        events = cursor.fetchall()
        conn.close()
        return [
            {"id": row[0], "action": row[1], "calendar_id": row[2], "name": row[3], "owner": row[4], "timestamp": row[5]}
            for row in events
        ]

    def get_event_count(self):
        conn = psycopg2.connect(self.database_url)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM events")
        count = cursor.fetchone()[0]
        conn.close()
        return count


    def get_events_by_owner(self, owner: str):
        conn = psycopg2.connect(self.database_url)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events WHERE owner = %s", (owner,))
        events = cursor.fetchall()
        conn.close()
        return [
            {"id": row[0], "action": row[1], "calendar_id": row[2], "name": row[3], "owner": row[4], "timestamp": row[5]}
            for row in events
        ]

    def get_events_by_action(self, action: str):
        conn = psycopg2.connect(self.database_url)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM events WHERE action = %s", (action.upper(),)
        )
        events = cursor.fetchall()
        conn.close()
        return [
            {"id": row[0], "action": row[1], "calendar_id": row[2], "name": row[3], "owner": row[4],
             "timestamp": row[5]}
            for row in events
        ]
