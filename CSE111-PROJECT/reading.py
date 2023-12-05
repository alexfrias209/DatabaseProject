import sqlite3

with open('z_database_scripts/test20.sql', 'r') as sql_file:
    sql_script = sql_file.read()

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

cursor.executescript(sql_script)

conn.commit()
conn.close()
