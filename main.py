"""Weather Dashboard - command-line menu (entry point)."""
import random
from datetime import datetime, timedelta

import analytics
import charts
from api_client import WeatherAPIError, fetch_current_weather
from models import WeatherRecord
from storage import HistoryStore

MENU = """
========== WEATHER DASHBOARD ==========
1. Check current weather (and save it)
2. View saved history for a city
3. Show temperature summary (high/low/avg)
4. Line chart (temperature & humidity)
5. Bar chart (temperature)
6. Export history to CSV
7. Delete a city's history
8. Add demo data (for testing charts)
0. Exit
=======================================
"""


def ask_city(store):
    """Ask for a city name, showing cities that already have history."""
    known = store.cities()
    if known:
        print("Saved cities:", ", ".join(known))
    return input("Enter city name: ").strip()


def check_weather(store):
    city = input("Enter city name: ").strip()
    if not city:
        print("City name cannot be empty.")
        return
    try:
        record = fetch_current_weather(city)
    except WeatherAPIError as err:
        print(f"Error: {err}")
        return
    print("\n" + str(record))
    store.add(record)
    print("\nSaved to history.")


def view_history(store):
    city = ask_city(store)
    records = store.get_city(city)
    if not records:
        print(f"No saved data for '{city}'.")
        return
    print(f"\n{'Date/Time':<20}{'Temp °C':>9}{'Humid %':>9}{'Wind':>8}{'hPa':>7}  Condition")
    for r in records:
        print(f"{r.timestamp:<20}{r.temperature:>9.1f}{r.humidity:>9.0f}"
              f"{r.wind_speed:>8.1f}{r.pressure:>7.0f}  {r.description}")


def show_summary(store):
    city = ask_city(store)
    analytics.print_summary(city, analytics.summarize(store.get_city(city)))


def show_chart(store, kind):
    city = ask_city(store)
    records = store.get_city(city)
    if not records:
        print(f"No saved data for '{city}'.")
        return
    (charts.line_chart if kind == "line" else charts.bar_chart)(city, records)


def export_csv(store):
    count = store.export_csv()
    print(f"Exported {count} records." if count else "Nothing to export.")


def delete_history(store):
    city = ask_city(store)
    if input(f"Delete ALL data for '{city}'? (y/n): ").lower() == "y":
        print(f"Removed {store.clear_city(city)} records.")


def add_demo_data(store):
    """Create 7 days of fake readings so charts can be tested offline."""
    city = input("Demo city name: ").strip() or "DemoCity"
    base = random.uniform(24, 34)
    for days_ago in range(6, -1, -1):
        when = datetime.now() - timedelta(days=days_ago)
        store.add(WeatherRecord(
            city, "Demo", base + random.uniform(-4, 4), random.uniform(35, 85),
            random.uniform(5, 25), random.uniform(1000, 1018), "Demo data",
            timestamp=when.strftime(WeatherRecord.TIME_FORMAT)))
    print("Added 7 demo records.")


def main():
    store = HistoryStore()
    actions = {
        "1": check_weather,
        "2": view_history,
        "3": show_summary,
        "4": lambda s: show_chart(s, "line"),
        "5": lambda s: show_chart(s, "bar"),
        "6": export_csv,
        "7": delete_history,
        "8": add_demo_data,
    }
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action(store)
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram stopped.")
