"""Chart generation with matplotlib (saved as PNG and shown on screen)."""
import os

import matplotlib
import matplotlib.pyplot as plt

import config


def _finish(fig, filename):
    """Save the figure to the charts folder, then try to display it."""
    os.makedirs(config.CHART_DIR, exist_ok=True)
    path = os.path.join(config.CHART_DIR, filename)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    print(f"Chart saved to: {path}")
    if matplotlib.get_backend().lower() != "agg":
        plt.show()
    plt.close(fig)


def line_chart(city, records):
    """Line chart of temperature and humidity over time."""
    if len(records) < 2:
        print("Need at least 2 records to draw a trend chart.")
        return
    times = [r.get_datetime() for r in records]
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(times, [r.temperature for r in records],
             color="tab:red", marker="o", label="Temperature (°C)")
    ax1.set_ylabel("Temperature (°C)", color="tab:red")
    ax2 = ax1.twinx()
    ax2.plot(times, [r.humidity for r in records],
             color="tab:blue", marker="s", label="Humidity (%)")
    ax2.set_ylabel("Humidity (%)", color="tab:blue")
    ax1.set_title(f"Temperature & Humidity Trend - {city}")
    ax1.set_xlabel("Date / Time")
    fig.autofmt_xdate()
    _finish(fig, f"{city.lower().replace(' ', '_')}_line.png")


def bar_chart(city, records):
    """Bar chart of temperature for each saved record."""
    if not records:
        print("No records to chart.")
        return
    labels = [r.get_datetime().strftime("%d %b\n%H:%M") for r in records]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(labels, [r.temperature for r in records], color="orange")
    ax.set_title(f"Temperature per Record - {city}")
    ax.set_ylabel("Temperature (°C)")
    _finish(fig, f"{city.lower().replace(' ', '_')}_bar.png")
