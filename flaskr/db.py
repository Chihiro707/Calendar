import sqlite3

DATABASE = "database.db"

def create_events_table():
    con = sqlite3.connect(DATABASE)
    con.execute("CREATE TABLE IF NOT EXISTS events(title, date, start_time, end_time, description)")
    con.close()