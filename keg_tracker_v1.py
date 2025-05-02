"""
Keg Tracker Application
======================

A Flask-based web application for tracking keg inventory. This application allows users to:
- Add new kegs with their type (Sixtel or Half Barrel), location, and status (Full or Empty)
- View all existing kegs in a table format
- Update the location and status of existing kegs
- Delete kegs from the inventory
- Create NFTs for kegs on the blockchain

The application uses SQLite as its database backend and provides a simple web interface
for managing keg inventory.

Database Schema:
---------------
The application uses a single table 'kegs' with the following columns:
- id: INTEGER PRIMARY KEY AUTOINCREMENT
- keg_type: TEXT NOT NULL (Sixtel or Half Barrel)
- location: TEXT NOT NULL
- status: TEXT NOT NULL (Full or Empty)

Usage:
------
1. Run the application: python keg_tracker_v1.py
2. Access the web interface at http://127.0.0.1:5000
3. Use the web interface to manage keg inventory

Dependencies:
------------
- Flask==3.0.2
- Werkzeug==3.0.1
"""

from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from blockchain import KegNFT
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Initialize blockchain connection
try:
    nft_manager = KegNFT()
    blockchain_enabled = True
except Exception as e:
    print(f"Blockchain initialization failed: {e}")
    blockchain_enabled = False

# Database configuration
DATABASE = 'keg_tracking.db'

def init_db():
    """
    Initialize the SQLite database and create the kegs table if it doesn't exist.
    
    This function:
    1. Connects to the SQLite database
    2. Creates a cursor object
    3. Executes the CREATE TABLE statement
    4. Commits the changes
    
    The kegs table has the following structure:
    - id: Auto-incrementing primary key
    - keg_type: Type of keg (Sixtel or Half Barrel)
    - location: Current location of the keg
    - status: Current status (Full or Empty)
    """
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS kegs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keg_type TEXT NOT NULL,
                location TEXT NOT NULL,
                status TEXT NOT NULL,
                nft_token_id TEXT
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    """
    Render the main page displaying all kegs.
    
    Returns:
        Rendered template with all kegs from the database.
    """
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM kegs')
        kegs = cursor.fetchall()
    return render_template('index.html', kegs=kegs, blockchain_enabled=blockchain_enabled)

@app.route('/add_keg', methods=['POST'])
def add_keg():
    """
    Add a new keg to the database and optionally create an NFT.
    
    This function:
    1. Retrieves form data (keg_type, location, status)
    2. Inserts the new keg into the database
    3. Redirects back to the main page
    
    Returns:
        Redirect to the index page after adding the keg.
    """
    keg_type = request.form['keg_type']
    location = request.form['location']
    status = request.form['status']
    
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO kegs (keg_type, location, status) VALUES (?, ?, ?)', 
                      (keg_type, location, status))
        keg_id = cursor.lastrowid
        
        # Create NFT if blockchain is enabled
        if blockchain_enabled and request.form.get('create_nft') == 'on':
            try:
                tx_hash = nft_manager.mint_nft(keg_id, keg_type, location, status)
                cursor.execute('UPDATE kegs SET nft_token_id = ? WHERE id = ?', 
                             (tx_hash, keg_id))
                flash(f'NFT created successfully! Transaction hash: {tx_hash}')
            except Exception as e:
                flash(f'Failed to create NFT: {str(e)}')
        
        conn.commit()
    return redirect(url_for('index'))

@app.route('/update_keg/<int:keg_id>', methods=['POST'])
def update_keg(keg_id):
    """
    Update an existing keg's location and status.
    
    Args:
        keg_id: The ID of the keg to update
        
    This function:
    1. Retrieves new location and status from the form
    2. Updates the keg in the database
    3. Redirects back to the main page
    
    Returns:
        Redirect to the index page after updating the keg.
    """
    location = request.form['location']
    status = request.form['status']
    
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE kegs SET location = ?, status = ? WHERE id = ?', 
                      (location, status, keg_id))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/delete_keg/<int:keg_id>', methods=['POST'])
def delete_keg(keg_id):
    """
    Delete a keg from the database.
    
    Args:
        keg_id: The ID of the keg to delete
        
    This function:
    1. Deletes the specified keg from the database
    2. Redirects back to the main page
    
    Returns:
        Redirect to the index page after deleting the keg.
    """
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM kegs WHERE id = ?', (keg_id,))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Initialize the database and start the Flask application
    init_db()
    app.run(debug=True)