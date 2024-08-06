import sqlite3

sqliteConnection = sqlite3.connect('JUEGO.db')
cursor = sqliteConnection.cursor()

query = 'Select sqlite_version();'
cursor.execute(query)

result = cursor.fetchall()
print('Version SQLite {}'.format(result))

cursor.close()