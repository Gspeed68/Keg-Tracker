# Keg Tracker

A Flask-based web application for tracking keg inventory. This application provides a simple and efficient way to manage your keg inventory, including tracking keg types, locations, and status.

## Features

- Add new kegs with type (Sixtel or Half Barrel), location, and status (Full or Empty)
- View all kegs in a clean, tabular format
- Update keg locations and status
- Delete kegs from inventory
- Simple and intuitive web interface
- SQLite database backend for reliable data storage

## Prerequisites

- Python 3.x
- pip (Python package installer)

## Installation

1. Clone or download this repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the application:
   ```bash
   python keg_tracker_v1.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

3. Use the web interface to:
   - Add new kegs using the form at the top
   - View all existing kegs in the table
   - Update keg locations and status
   - Delete kegs as needed

## Database Structure

The application uses a SQLite database with the following table structure:

```sql
CREATE TABLE kegs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keg_type TEXT NOT NULL,
    location TEXT NOT NULL,
    status TEXT NOT NULL
)
```

- `id`: Auto-incrementing primary key
- `keg_type`: Type of keg (Sixtel or Half Barrel)
- `location`: Current location of the keg
- `status`: Current status (Full or Empty)

## Dependencies

- Flask==3.0.2
- Werkzeug==3.0.1

## Development

The application is built using:
- Flask for the web framework
- SQLite for the database
- HTML/CSS for the frontend
- Jinja2 for templating

## Contributing

Feel free to submit issues and enhancement requests.

## License

This project is open source and available under the MIT License.

## Support

For support, please open an issue in the GitHub repository. 