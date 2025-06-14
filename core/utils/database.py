# database.py

import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="focus_forge.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # Sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                work_duration_planned INTEGER,
                work_duration_actual REAL,
                break_taken INTEGER,
                break_duration INTEGER,
                task TEXT,
                completed INTEGER,
                distraction_events INTEGER,
                timestamp TEXT
            )
        ''')
        # Tasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                priority INTEGER DEFAULT 1,
                estimated_time INTEGER DEFAULT 25,
                completed INTEGER DEFAULT 0,
                created_at TEXT
            )
        ''')
        # Board state table (single-row JSON payload)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS board_state (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                state_json TEXT,
                updated_at TEXT
            )
        ''')
        self.conn.commit()

    # Session Methods
    def log_session(self, work_planned, work_actual, break_taken, break_duration, task, completed, distractions):
        cursor = self.conn.cursor()
        timestamp = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO sessions (
                work_duration_planned, work_duration_actual, break_taken,
                break_duration, task, completed, distraction_events, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (work_planned, work_actual, break_taken, break_duration, task, completed, distractions, timestamp))
        self.conn.commit()

    def get_recent_sessions(self, limit=10):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM sessions ORDER BY id DESC LIMIT ?
        ''', (limit,))
        return cursor.fetchall()

    def get_success_rate(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM sessions WHERE completed=1
        ''')
        completed = cursor.fetchone()[0]
        cursor.execute('''
            SELECT COUNT(*) FROM sessions
        ''')
        total = cursor.fetchone()[0]
        return (completed / total) * 100 if total > 0 else 0

    def get_consecutive_failures(self, threshold=3):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT completed FROM (
                SELECT completed FROM sessions ORDER BY id DESC LIMIT ?
            )
        ''', (threshold,))
        results = cursor.fetchall()
        return all(r[0] == 0 for r in results) if len(results) == threshold else False

    def get_streak(self, limit=5):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT completed FROM sessions ORDER BY id DESC LIMIT ?
        ''', (limit,))
        results = cursor.fetchall()
        streak = 0
        for r in results:
            if r[0] == 1:
                streak += 1
            else:
                break
        return streak

    def get_average_work_duration(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT AVG(work_duration_actual) FROM sessions WHERE completed=1
        ''')
        result = cursor.fetchone()[0]
        return round(result, 2) if result else 0.0

    def get_average_distractions(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT AVG(distraction_events) FROM sessions
        ''')
        result = cursor.fetchone()[0]
        return round(result, 2) if result else 0.0

    # Task Methods
    def add_task(self, description, priority=1, estimated_time=25):
        cursor = self.conn.cursor()
        created_at = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO tasks (description, priority, estimated_time, completed, created_at)
            VALUES (?, ?, ?, 0, ?)
        ''', (description, priority, estimated_time, created_at))
        self.conn.commit()

    def get_pending_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM tasks WHERE completed=0 ORDER BY priority DESC, created_at ASC
        ''')
        return cursor.fetchall()

    def complete_task(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE tasks SET completed=1 WHERE id=?
        ''', (task_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

    # ------------------------------------------------------------------
    # Kanban Board (KantuBoard) persistence helpers
    # ------------------------------------------------------------------

    def save_board_state(self, state_dict):
        """Persist full board state (dict) as JSON in the single-row table."""
        import json, datetime
        payload = json.dumps(state_dict, indent=2)
        ts = datetime.datetime.now().isoformat()
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO board_state (id, state_json, updated_at)
            VALUES (1, ?, ?)
            ON CONFLICT(id) DO UPDATE SET state_json = excluded.state_json, updated_at = excluded.updated_at
        ''', (payload, ts))
        self.conn.commit()

    def load_board_state(self):
        """Return board state dict if stored, else None."""
        import json
        cursor = self.conn.cursor()
        cursor.execute('SELECT state_json FROM board_state WHERE id = 1')
        row = cursor.fetchone()
        return json.loads(row[0]) if row and row[0] else None
