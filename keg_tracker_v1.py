# app.py
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
DATABASE = 'keg_tracking.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS kegs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keg_type TEXT NOT NULL,
                location TEXT NOT NULL,
                status TEXT NOT NULL
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM kegs')
        kegs = cursor.fetchall()
    return render_template('index.html', kegs=kegs)

@app.route('/add_keg', methods=['POST'])
def add_keg():
    keg_type = request.form['keg_type']
    location = request.form['location']
    status = request.form['status']
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO kegs (keg_type, location, status) VALUES (?, ?, ?)', (keg_type, location, status))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/update_keg/<int:keg_id>', methods=['POST'])
def update_keg(keg_id):
    location = request.form['location']
    status = request.form['status']
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE kegs SET location = ?, status = ? WHERE id = ?', (location, status, keg_id))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/delete_keg/<int:keg_id>', methods=['POST'])
def delete_keg(keg_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM kegs WHERE id = ?', (keg_id,))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)