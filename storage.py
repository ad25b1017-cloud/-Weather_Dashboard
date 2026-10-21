"""Local storage: saves weather history to JSON and exports to CSV."""
import csv
import json
import os

import config
from models import WeatherRecord


class HistoryStore:
    """Reads and writes WeatherRecord objects to a JSON file."""

    def __init__(self, path=config.HISTORY_FILE):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    def load_all(self):
        """Return every saved record as a list (empty if file missing/corrupt)."""
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return [WeatherRecord.from_dict(d) for d in json.load(f)]
        except FileNotFoundError:
            return []
        except (json.JSONDecodeError, TypeError, KeyError):
            print("Warning: history file is corrupted. Starting fresh.")
            return []

    def _write(self, records):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([r.to_dict() for r in records], f, indent=2)

    def add(self, record):
        """Append one record to history."""
        records = self.load_all()
        records.append(record)
        self._write(records)

    def get_city(self, city):
        """Return records for a city (case-insensitive), oldest first."""
        matches = [r for r in self.load_all() if r.city.lower() == city.lower()]
        return sorted(matches, key=lambda r: r.get_datetime())

    def cities(self):
        """Return a sorted list of unique city names in history."""
        return sorted({r.city for r in self.load_all()})

    def clear_city(self, city):
        """Delete all records of a city; return how many were removed."""
        records = self.load_all()
        kept = [r for r in records if r.city.lower() != city.lower()]
        self._write(kept)
        return len(records) - len(kept)

    def export_csv(self, path=config.CSV_FILE):
        """Write all history to a CSV file and return the row count."""
        records = self.load_all()
        if not records:
            return 0
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(records[0].to_dict().keys()))
            writer.writeheader()
            writer.writerows(r.to_dict() for r in records)
        return len(records)
