import sqlite3 as sq

conn = sq.connect('database.db')
cur = conn.cursor()

table = '''CREATE TABLE IF NOT EXISTS activities(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name VARCHAR NOT NULL,
activity_type VARCHAR NOT NULL,
duration REAL,
distance REAL,
date DATE)'''

cur.execute(table)