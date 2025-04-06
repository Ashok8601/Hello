from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime
from init_db import init_db
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database Setup
def get_db_connection():
    conn = sqlite3.connect('fake.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['GET', 'POST'])
@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    pages = []
    today = datetime.now().date().isoformat()

    # Static URLs
    pages.append(['/', today])
    pages.append(['/about', today])
    pages.append(['/contact', today])

    # Dynamic URLs from fake.db -> fake table using `username`
    try:
        conn = sqlite3.connect('fake.db')
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM fake")
        rows = cursor.fetchall()

        for (username,) in rows:
            pages.append([f'/user/{username}', today])  # assuming URL structure like /user/username
        conn.close()
    except Exception as e:
        print("DB Error:", e)

    # Build XML
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for page, date in pages:
        sitemap_xml += '  <url>\n'
        sitemap_xml += f'    <loc>https://you-tube-atr0.onrender.com{page}</loc>\n'
        sitemap_xml += f'    <lastmod>{date}</lastmod>\n'
        sitemap_xml += '    <changefreq>monthly</changefreq>\n'
        sitemap_xml += '    <priority>0.8</priority>\n'
        sitemap_xml += '  </url>\n'

    sitemap_xml += '</urlset>'
    return Response(sitemap_xml, mimetype='application/xml')
    
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

@app.route('/')
def home():
    return render_template('home.html')
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
