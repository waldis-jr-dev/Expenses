import sqlite3
import data

conn = sqlite3.connect(data.DB_URL)
cursor = conn.cursor()

cursor.executescript('''CREATE TABLE IF NOT EXISTS expense (
	id integer PRIMARY KEY AUTOINCREMENT,
	name text,
	datetime integer,
	type text,
	amount float
)
''')

conn.commit()
cursor.close()
conn.close()
