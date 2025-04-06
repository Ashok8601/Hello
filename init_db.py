import sqlite3
def init_db():
    conn = sqlite3.connect('fake.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS fake (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
if __name__ == '__main__':
    init_db()
    app.run(debug=True)