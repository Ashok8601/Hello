from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from init_db import init_db
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database Setup
def get_db_connection():
    conn = sqlite3.connect('fake.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
    
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO fake ( username, password) VALUES (?, ?)', 
                         ( username, password))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Username already exists!"
        finally:
            conn.close()

        return "invalid email or password"

    return render_template('login.html')

@app.route('/home')
def home():
    if 'user' in session:
        return render_template('home.html', email=session['user'])
    return redirect(url_for('login'))

@app.route('/admin')
def show_users():
    conn = sqlite3.connect('fake.db')  # Replace with your .db name
    cur = conn.cursor()
    cur.execute("SELECT * FROM fake")  # Replace with your actual table name
    users = cur.fetchall()
    conn.close()
    return render_template("admin.html", users=users)

if __name__ == '__main__':
    app.run(debug=True)