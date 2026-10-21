"""Statistics calculated from saved weather records."""


def summarize(records):
    """Return highest/lowest/average temperature (and avg humidity) for records.

    Returns None when there are no records.
    """
    if not records:
        return None
    temps = [r.temperature for r in records]
    hums = [r.humidity for r in records]
    hottest = max(records, key=lambda r: r.temperature)
    coldest = min(records, key=lambda r: r.temperature)
    return {
        "count": len(records),
        "max_temp": hottest.temperature,
        "max_time": hottest.timestamp,
        "min_temp": coldest.temperature,
        "min_time": coldest.timestamp,
        "avg_temp": sum(temps) / len(temps),
        "avg_humidity": sum(hums) / len(hums),
    }


def print_summary(city, stats):
    """Pretty-print the dictionary returned by summarize()."""
    if stats is None:
        print("No data to summarize.")
        return
    print(f"\n--- Summary for {city} ({stats['count']} records) ---")
    print(f"Highest temp : {stats['max_temp']:.1f} °C  at {stats['max_time']}")
    print(f"Lowest temp  : {stats['min_temp']:.1f} °C  at {stats['min_time']}")
    print(f"Average temp : {stats['avg_temp']:.1f} °C")
    print(f"Avg humidity : {stats['avg_humidity']:.1f} %")
