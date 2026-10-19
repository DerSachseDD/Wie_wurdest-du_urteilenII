"""Load editable case data from JSON and synchronize it to SQLite."""
import json
from pathlib import Path
from app import db
from app.models import Case

DATA_FILE = Path(__file__).with_name("data.json")


def load_cases():
    """Read and validate the case list from data.json."""
    with DATA_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise ValueError("cases/data.json must contain a JSON array")

    required = {"id", "title", "description", "real_sentence", "category"}
    for item in data:
        missing = required - item.keys()
        if missing:
            raise ValueError(f"Case is missing required fields: {sorted(missing)}")
    return data


def sync_cases_to_database():
    """Insert new cases and update existing ones without deleting votes."""
    for item in load_cases():
        case = db.session.get(Case, int(item["id"]))
        values = {
            "title": item["title"],
            "description": item["description"],
            "real_sentence": item["real_sentence"],
            "category": item["category"],
            "real_fine": float(item.get("real_fine", 0)),
            "real_jail": float(item.get("real_jail", 0)),
        }
        if case is None:
            case = Case(id=int(item["id"]), **values)
            db.session.add(case)
        else:
            for key, value in values.items():
                setattr(case, key, value)
    db.session.commit()
