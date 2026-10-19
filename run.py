"""Development entry point: run with `python run.py`."""
from pathlib import Path
from app import create_app

# Ensure SQLite's parent directory exists before SQLAlchemy opens the database.
Path("instance").mkdir(exist_ok=True)

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
