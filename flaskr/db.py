import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "database.db"

def get_connection():
    """
    データベースへの接続を取得する。
    """

    return sqlite3.connect(DATABASE)


def create_events_table():
    """
    eventsテーブルが存在しなければ作成する。
    """

    con = get_connection()
    con.execute("""
        CREATE TABLE IF NOT EXISTS events(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            start_time TEXT,
            end_time TEXT,
            description TEXT
        )
    """)
    con.close()

# Create
def add_event(title, date, start_time, end_time, description):
    """
    新しい予定を追加する。
    """

    con = get_connection()
    con.execute("""
        INSERT INTO events (title, date, start_time, end_time, description)
        VALUES (?, ?, ?, ?, ?)
    """, (title, date, start_time, end_time, description))
    con.commit()
    con.close()

# Read
def get_dates_with_events(event_id=None):
    """
    event_idが指定されていない場合、予定がある日付を取得する。
    event_idが指定されている場合、指定されたIDの予定の日付を取得する。
    """

    if event_id is None:
        con = get_connection()
        con.row_factory = sqlite3.Row
        dates = con.execute(
            'SELECT DISTINCT date FROM events ORDER BY date'
        ).fetchall()
        con.close()

        return dates

    else:
        con = get_connection()
        con.row_factory = sqlite3.Row
        date = con.execute(
            'SELECT date FROM events WHERE id = ?',
            (event_id,)
        ).fetchone()
        con.close()

        if date is None:
            return None

        return date

def get_events_by_date(date):
    """
    指定された日付の予定をすべて取得する。
    """

    con = get_connection()
    con.row_factory = sqlite3.Row
    events = con.execute(
        'SELECT * FROM events WHERE date = ? ORDER BY start_time',
        (date,)
    ).fetchall()
    con.close()

    return events

def get_event_by_id(event_id):
    """
    指定されたIDの予定を取得する。
    """

    con = get_connection()
    con.row_factory = sqlite3.Row
    event = con.execute(
        'SELECT * FROM events WHERE id = ?',
        (event_id,)
    ).fetchone()
    con.close()

    return event

# Update
def update_event(event_id, title, date, start_time, end_time, description):
    """
    指定されたIDの予定を更新する。
    """

    con = get_connection()
    con.execute("""
        UPDATE events
        SET title = ?, date = ?, start_time = ?, end_time = ?, description = ?
        WHERE id = ?
    """, (title, date, start_time, end_time, description, event_id))
    con.commit()
    con.close()

# Delete
def delete_event(event_id):
    """
    指定されたIDの予定を削除する。
    """

    con = get_connection()
    con.execute(
        'DELETE FROM events WHERE id = ?',
        (event_id,)
    )
    con.commit()
    con.close()